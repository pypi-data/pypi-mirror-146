import base64
import hmac
import json
import uuid
from hashlib import sha256
from typing import Any, Dict, Optional

import requests

from fastel.payment.linepay.model import LinePayRequestModel


class LinePay:
    @property
    def linepay_url(self) -> str:
        if self.stage in ["prod", "PROD"]:
            return "https://api-pay.line.me"
        return "https://sandbox-api-pay.line.me"

    def __init__(
        self,
        stage: str,
        channel_id: str,
        channel_secret: str,
        api_host: str,
    ):
        self.stage = stage
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.api_host = api_host

    def build_headers(
        self,
        uri: str,
        request_body: str,
    ) -> Dict[str, Any]:
        nonce = str(uuid.uuid4())
        _signature = hmac.new(
            key=self.channel_secret.encode(),
            msg=(self.channel_secret + uri + request_body + nonce).encode(),
            digestmod=sha256,
        )
        signature = base64.b64encode(_signature.digest()).decode()
        return {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": self.channel_id,
            "X-LINE-Authorization-Nonce": nonce,
            "X-LINE-Authorization": signature,
        }

    def request(self, data: LinePayRequestModel) -> Any:
        body = data.dict(exclude_none=True)
        json_str = json.dumps(body)
        path = "/v3/payments/request"
        url = f"{self.linepay_url}{path}"
        headers = self.build_headers(path, json_str)
        resp = requests.post(
            url=url,
            json=body,
            headers=headers,
        )
        return resp.json()

    def confirm(self, transaction_id: str, amount: int) -> Any:
        body = {"amount": amount, "currency": "TWD"}
        json_str = json.dumps(body)
        path = f"/v3/payments/{transaction_id}/confirm"
        url = f"{self.linepay_url}{path}"
        headers = self.build_headers(path, json_str)
        resp = requests.post(url=url, json=body, headers=headers)
        return resp.json()

    def refund(self, transaction_id: str, refund_amount: int) -> Any:
        body = {"refundAmount": refund_amount}
        json_str = json.dumps(body)
        path = f"/v3/payments/{transaction_id}/refund"
        url = f"{self.linepay_url}{path}"
        headers = self.build_headers(path, json_str)
        resp = requests.post(
            url=url,
            json=body,
            headers=headers,
        )
        return resp.json()

    def get_details(
        self, transaction_id: Optional[str] = None, order_id: Optional[str] = None
    ) -> Any:
        path = f"/v3/payments"
        query = ""
        if transaction_id is not None:
            query += "transactionId={}&".format(str(transaction_id))
        if order_id is not None:
            query += "orderId={}".format(order_id)
        if query.endswith("?") or query.endswith("&"):
            query = query[:-1]

        url = (
            f"{self.linepay_url}{path}?{query}"
            if query
            else f"{self.linepay_url}{path}"
        )
        headers = self.build_headers(path, query)
        resp = requests.get(
            url=url,
            headers=headers,
        )
        return resp.json()
