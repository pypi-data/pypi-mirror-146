import base64
import hmac
import json
import uuid
from hashlib import sha256
from typing import Any, Dict, List, Optional

import requests

from fastel.payment.linepay.exceptions import LinePayException


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
    ):
        self.stage = stage
        self.channel_id = channel_id
        self.channel_secret = channel_secret

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

    @staticmethod
    def to_products(
        items: List[Dict[str, Any]] = [],
        fee_items: List[Dict[str, Any]] = [],
        discount_items: List[Dict[str, Any]] = [],
    ) -> List[Dict[str, Any]]:
        products_array = []
        if items is []:
            raise LinePayException(
                error="item_empty_error", detail="item should not be empty"
            )
        for item in items:
            products_array.append(
                dict(
                    id=item["product"]["id"]["$oid"],
                    name=item["name"],
                    imageUrl=item["product"]["images"][0]["expected_url"],
                    quantity=item["config"]["qty"],
                    price=item["price"],
                )
            )

        for fee in fee_items:
            products_array.append(
                dict(
                    id=str(uuid.uuid4()),
                    name=fee["name"],
                    imageUrl="",
                    quantity=1,
                    price=fee["amount"],
                )
            )

        for discount in discount_items:
            products_array.append(
                dict(
                    id=str(uuid.uuid4()),
                    name=discount["name"],
                    imageUrl="",
                    quantity=1,
                    price=-discount["amount"],
                )
            )

        return products_array

    def request(
        self,
        order_id: str,
        currency: str,
        order_total: int,
        order_items: List[Any],
        callback_url: str,
    ) -> Any:
        body = {
            "amount": order_total,
            "currency": currency,
            "orderId": order_id,
            "packages": order_items,
            "redirectUrls": {
                "confirmUrl": callback_url,
                "cancelUrl": callback_url,
            },
        }
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
