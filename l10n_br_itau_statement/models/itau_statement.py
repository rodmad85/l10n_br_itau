from odoo import models, fields
from datetime import date

class ItauStatement(models.Model):
    _name = "itau.statement"
    _description = "Importação Extrato Itaú"

    name = fields.Char(default="Importação Itaú")
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    account_number = fields.Char(required=True)

    def action_import_statement(self):
        service = self.env["itau.api.service"]

        params = {
            "type": "current_account",
            "start_date": self.date_start.strftime("%Y-%m-%d"),
            "end_date": self.date_end.strftime("%Y-%m-%d"),
        }

        data = service.request(
            "GET",
            f"/accounts/v1/statements/{self.account_number}",
            params=params
        )

        self._create_bank_statement(data)

    def _create_bank_statement(self, data):
        journal = self.env["account.journal"].search(
            [("type", "=", "bank")], limit=1
        )

        statement = self.env["account.bank.statement"].create({
            "journal_id": journal.id,
            "date": fields.Date.today(),
        })

        for tx in data.get("transactions", []):
            self.env["account.bank.statement.line"].create({
                "statement_id": statement.id,
                "date": tx.get("date"),
                "payment_ref": tx.get("description"),
                "amount": tx.get("amount"),
            })