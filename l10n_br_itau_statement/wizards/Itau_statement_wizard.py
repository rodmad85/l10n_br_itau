from odoo import models, fields

class ItauStatementWizard(models.TransientModel):
    _name = "itau.statement.wizard"
    _description = "Wizard Importação Itaú"

    journal_id = fields.Many2one("account.journal", required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    def action_import(self):
        service = self.env["itau.api.service"]

        account_number = self.journal_id.bank_account_id.acc_number

        data = service.request(
            "GET",
            f"/accounts/v1/statements/{account_number}",
            params={
                "start_date": self.date_start.strftime("%Y-%m-%d"),
                "end_date": self.date_end.strftime("%Y-%m-%d"),
            }
        )

        self._create_statement(data)

    def _create_statement(self, data):
        statement = self.env["account.bank.statement"].create({
            "journal_id": self.journal_id.id,
            "date": fields.Date.today(),
        })

        for tx in data.get("transactions", []):
            self.env["account.bank.statement.line"].create({
                "statement_id": statement.id,
                "date": tx.get("date"),
                "payment_ref": tx.get("description"),
                "amount": tx.get("amount"),
            })