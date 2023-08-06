from nautobot.extras.plugins import PluginTemplateExtension


class DeepCopyTemplate(PluginTemplateExtension):
    model = "dcim.device"

    def buttons(self):
        device = self.context["object"]

        return self.render(
            "nautobot_deepcopy/inc/buttons.html",
            {
                "device": device,
            },
        )


template_extensions = [DeepCopyTemplate]
