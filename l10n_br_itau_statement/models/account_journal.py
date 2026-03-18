from odoo import models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    def action_open_itau_import_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Importar Extrato Itaú",
            "res_model": "itau.statement.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_journal_id": self.id,
            },
        }