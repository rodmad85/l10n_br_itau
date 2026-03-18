from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    itau_client_id = fields.Char(string="Client ID")
    itau_client_secret = fields.Char(string="Client Secret")
    itau_api_key = fields.Char(string="API Key")
    itau_environment = fields.Selection(
        [("sandbox", "Sandbox"), ("prod", "Produção")],
        default="sandbox"
    )

    def set_values(self):
        super().set_values()
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param("itau.client_id", self.itau_client_id)
        ICP.set_param("itau.client_secret", self.itau_client_secret)
        ICP.set_param("itau.api_key", self.itau_api_key)
        ICP.set_param("itau.environment", self.itau_environment)

    def get_values(self):
        res = super().get_values()
        ICP = self.env["ir.config_parameter"].sudo()
        res.update({
            "itau_client_id": ICP.get_param("itau.client_id"),
            "itau_client_secret": ICP.get_param("itau.client_secret"),
            "itau_api_key": ICP.get_param("itau.api_key"),
            "itau_environment": ICP.get_param("itau.environment"),
        })
        return res
