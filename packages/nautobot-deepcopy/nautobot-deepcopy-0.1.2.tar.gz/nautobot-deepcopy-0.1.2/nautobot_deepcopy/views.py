from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.html import escape
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from django.views.generic import View

from nautobot.dcim.models import Device
from nautobot.core.views.generic import GetReturnURLMixin

from .forms import CopyForm


class CopyView(PermissionRequiredMixin, GetReturnURLMixin, View):
    permission_required = "dcim.add_device"
    template_name = "nautobot_deepcopy/copy.html"

    def get(self, request, *args, pk=None, **kwargs):
        device = Device.objects.get(pk=pk)
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}
        initial_data["region"] = device.site.region
        initial_data["site"] = device.site
        initial_data["status"] = device.status
        initial_data["comments"] = device.comments
        initial_data["face"] = device.face
        initial_data["rack"] = device.rack

        form = CopyForm(initial=initial_data)

        return render(
            request,
            self.template_name,
            {
                "device": device,
                "form": form,
                "return_url": self.get_return_url(request, device),
            },
        )

    def post(self, request, *args, pk=None, **kwargs):
        device = Device.objects.get(pk=pk)
        form = CopyForm(request.POST, request.FILES, instance=device)

        if form.is_valid():
            copy = form.save()

            msg = 'Copied device <a href="{}">{}</a>'.format(
                copy.get_absolute_url(), escape(copy)
            )
            messages.success(request, mark_safe(msg))

            return_url = form.cleaned_data.get("return_url")
            if return_url is not None and is_safe_url(
                url=return_url, allowed_hosts=request.get_host()
            ):
                return redirect(return_url)
            return redirect(self.get_return_url(request, copy))

        return render(
            request,
            self.template_name,
            {
                "device": device,
                "form": form,
                "return_url": self.get_return_url(request, device),
            },
        )
