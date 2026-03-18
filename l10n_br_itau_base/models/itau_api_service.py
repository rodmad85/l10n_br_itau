import requests
import uuid
from odoo import models

class ItauApiService(models.AbstractModel):
    _name = "itau.api.service"
    _description = "Itau API Service"

    def _get_base_url(self):
        env = self.env["ir.config_parameter"].sudo().get_param("itau.environment")
        if env == "prod":
            return "https://api.itau.com.br"
        return "https://sandbox.devportal.itau.com.br"

    def _get_token_url(self):
        env = self.env["ir.config_parameter"].sudo().get_param("itau.environment")
        if env == "prod":
            return "https://sts.itau.com.br/api/oauth/token"
        return "https://sts.rdhi.com.br/api/oauth/token"

    def _get_token(self):
        ICP = self.env["ir.config_parameter"].sudo()
        client_id = ICP.get_param("itau.client_id")
        client_secret = ICP.get_param("itau.client_secret")

        response = requests.post(
            self._get_token_url(),
            data={
                "grant_type": "client_credentials",
            },
            auth=(client_id, client_secret),
        )

        response.raise_for_status()
        return response.json().get("access_token")

    def _headers(self):
        ICP = self.env["ir.config_parameter"].sudo()
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "x-itau-apikey": ICP.get_param("itau.api_key"),
            "x-itau-correlationid": str(uuid.uuid4()),
            "x-itau-flowid": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }

    def request(self, method, endpoint, params=None):
        url = f"{self._get_base_url()}{endpoint}"

        response = requests.request(
            method,
            url,
            headers=self._headers(),
            params=params,
        )

        response.raise_for_status()
        return response.json()
