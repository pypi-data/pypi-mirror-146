import time
from typing import Dict, List

import requests
from instabuy_integration_utils.config import config
from instabuy_integration_utils.models.IBBuy import IBBuy
from instabuy_integration_utils.utils.IBProductsLoadUtil import IBProductsLoadUtil


class IBRequest:

    @staticmethod
    def get_buys_ready_for_erp(ib_api_key: str) -> List[IBBuy]:
        response = requests.get(
            "https://api.instabuy.com.br/store/buys?status=erp_ready",
            headers={"api-key": ib_api_key},
        )
        if response.status_code != 200:
            raise Exception("Error on get_buys_ready_for_erp: {response.text}")
        else:
            buys: List[IBBuy] = []
            for buy_dict in response.json()["data"]:
                buys.append(IBBuy(buy_dict))

            return buys

    @staticmethod
    def update_buy_status(
        ib_api_key: str,
        new_status: str,
        request_author: str,
        erp_id=None,
        buy_id=None,
    ):
        body = {"status": new_status, "request_author": request_author}
        if erp_id:
            body["erp_id"] = int(erp_id)
        elif buy_id:
            body["id"] = str(buy_id)
        else:
            raise Exception("You must pass erp_id or buy_id")

        response = requests.put(
            "https://api.instabuy.com.br/store/buys",
            json=body,
            headers={"api-key": ib_api_key},
        )

        if response.status_code != 200:
            raise Exception(f"Error on update_buy_status: {response.text}")

    @staticmethod
    def send_products_to_api(ib_api_key: str, products: List[Dict]):
        if config.DEBUG:
            print("Items processed. Will send to API")

        outdated_products = IBProductsLoadUtil.get_outdated_products(
            ib_api_key, products
        )
        outdated_len = len(outdated_products)

        if outdated_len == 0:
            if config.DEBUG:
                print("There is none outdated product to send")

            return

        if config.DEBUG:
            print(
                f"Will send {outdated_len} outdated products from {len(products)} products"
            )

        products_count = 0
        while len(outdated_products) != 0:
            products_to_send = []

            for _ in range(
                0, min(config.items_batch_count, len(outdated_products)), +1
            ):
                products_to_send.append(outdated_products[0])
                outdated_products.pop(0)

            products_count += len(products_to_send)

            if config.DEBUG:
                init_time = time.time()
                print(f"Sending {products_count}/{outdated_len} products...")

            response = requests.put(
                "https://api.instabuy.com.br/store/products",
                json={"products": products_to_send},
                headers={"api-key": ib_api_key},
            )

            if response.status_code != 200:
                raise Exception(f"Error on send_products_to_api: {response.text}")

            if config.DEBUG:
                print(f"Request processed in {int(time.time() - init_time)} seconds")

        if config.DEBUG:
            print("Items updated")
