from collections import defaultdict

from django import forms
from django.db import transaction

from nautobot.extras.models import Status
from nautobot.utilities.forms import (
    APISelect,
    add_blank_choice,
    BootstrapMixin,
    CommentField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
)
from nautobot.dcim.choices import *
from nautobot.dcim.models import (
    Device,
    Rack,
    Region,
    Site,
)
from nautobot.extras.models import Tag


class CopyForm(BootstrapMixin, forms.Form):
    name = forms.CharField(
        max_length=100,
    )
    status = DynamicModelChoiceField(
        queryset=Status.objects.get_for_model(Device),
        required=True,
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(), required=False, initial_params={"sites": "$site"}
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=True,
        query_params={"region_id": "$region"},
    )
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        display_field="display_name",
        query_params={
            "site_id": "$site",
            "group_id": "$rack_group",
        },
    )
    position = forms.IntegerField(
        required=False,
        help_text="The lowest-numbered unit occupied by the device",
        widget=APISelect(
            api_url="/api/dcim/racks/{{rack}}/elevation/",
            attrs={
                "disabled-indicator": "device",
                "data-query-param-face": '["$face"]',
            },
        ),
    )
    face = forms.ChoiceField(
        choices=add_blank_choice(DeviceFaceChoices),
        required=False,
        help_text="Mounted rack face",
    )
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    comments = CommentField()

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance

        return super().__init__(*args, **kwargs)

    def clean(self):
        # validity check if another item has the same name
        used_site = self.cleaned_data.get("site")
        used_rack = self.cleaned_data.get("rack")
        used_face = self.cleaned_data.get("face")
        used_position = self.cleaned_data.get("position")
        if Device.objects.filter(
            name=self.cleaned_data["name"], site=used_site, tenant__isnull=True
        ).exists():
            raise forms.ValidationError(
                {"name": "A device with this name already exists."}
            )


        if used_rack and used_face and used_position and Device.objects.filter(
            rack=used_rack,
            face=used_face,
            position=used_position,
        ).exists():
            raise forms.ValidationError(
                {"face": "A device with this position and face already exists."}
            )

    @transaction.atomic
    def save(self):
        self.instance.name = self.cleaned_data["name"]

        self.instance.site = self.cleaned_data["site"]
        if self.cleaned_data["status"]:
            self.instance.status = self.cleaned_data["status"]
        self.instance.comments = self.cleaned_data["comments"]
        self.instance.face = self.cleaned_data.get("face")
        self.instance.position = self.cleaned_data.get("position")
        self.instance.rack = self.cleaned_data.get("rack")

        self.instance.virtual_chassis = None
        self.instance.vc_position = None
        self.instance.asset_tag = None
        self.instance.primary_ip4_id = None
        self.instance.primary_ip6_id = None

        tags = []
        components = defaultdict(list)
        children = {}

        for tag in self.instance.tags.all():
            tags.append(tag)

        for component_type in [
            "consoleports",
            "consoleserverports",
            "powerports",
            "poweroutlets",
            "interfaces",
            "rearports",
            "frontports",
            "devicebays",
        ]:
            prop = getattr(self.instance, component_type)
            for component in prop.all():
                components[component_type].append(component)

        for devicebay in self.instance.devicebays.all():
            child = devicebay.installed_device
            # only save children if available
            if child:
                child.pk = None
                child._state.adding = True
                child.name = None
                child.rack = self.cleaned_data.get("rack")
                child.primary_ip4_id = None
                child.primary_ip6_id = None
                if self.cleaned_data["status"]:
                    child.status = self.cleaned_data["status"]
                child.save()
            children[devicebay.name] = child

        self.instance.pk = None
        self.instance._state.adding = True
        self.instance.save()

        if self.cleaned_data["tags"].exists():
            for tag in self.cleaned_data["tags"].all():
                self.instance.tags.add(tag)
        else:
            for tag in tags:
                self.instance.tags.add(tag)

        for type_, component_list in components.items():
            prop = getattr(self.instance, type_)
            prop.all().delete()
            for component in component_list:
                component.device = self.instance
                component.pk = None
                component._state.adding = True
                component.cable = None
                component._cable_peer = None
                component._path = None
                if hasattr(component, "installed_device"):
                    child = children[component.name]
                    component.installed_device = child
                component.save()

        # the powerports in poweroutlets also need to be reset
        for poweroutlet in self.instance.poweroutlets.all():
            if not poweroutlet.power_port:
                continue
            # TODO: will this work in all cases?
            port = [
                p
                for p in components["powerports"]
                if p.name == poweroutlet.power_port.name
            ][0]
            poweroutlet.power_port = port
            poweroutlet.save()

        return self.instance
