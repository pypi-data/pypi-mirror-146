from nautobot.extras.plugins import PluginConfig


class DeepCopyConfig(PluginConfig):
    name = "nautobot_deepcopy"
    verbose_name = "Deep Copy"
    description = "A plugin for copying devices and their components"
    version = '0.1.2'
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = "nautobot_deepcopy"
    required_settings = []
    default_settings = {}
    middleware = []


config = DeepCopyConfig
