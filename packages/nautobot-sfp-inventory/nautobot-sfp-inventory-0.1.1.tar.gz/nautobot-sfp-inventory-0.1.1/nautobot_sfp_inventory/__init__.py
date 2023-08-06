from nautobot.extras.plugins import PluginConfig

class SFPInventoryConfig(PluginConfig):
    name = 'nautobot_sfp_inventory'
    verbose_name = 'SFP Inventory'
    description = 'A plugin for SFP inventory management'
    version = '0.1.1'
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot_sfp_inventory'

config = SFPInventoryConfig

