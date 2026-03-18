def _cron_import_itau_statements(self):
    journals = self.search([("type", "=", "bank")])

    for journal in journals:
        if not journal.bank_account_id:
            continue

        service = self.env["itau.api.service"]

        data = service.request(
            "GET",
            f"/accounts/v1/statements/{journal.bank_account_id.acc_number}",
            params={
                "start_date": fields.Date.today().strftime("%Y-%m-%d"),
                "end_date": fields.Date.today().strftime("%Y-%m-%d"),
            }
        )

        # reutiliza lógica
        wizard = self.env["itau.statement.wizard"].create({
            "journal_id": journal.id,
            "date_start": fields.Date.today(),
            "date_end": fields.Date.today(),
        })

        wizard._create_statement(data)