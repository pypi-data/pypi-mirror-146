import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List
from instabuy_integration_utils.config import config


class IBProductsLoadUtil:
    @staticmethod
    def get_outdated_products(ib_api_key: str, products: List[Dict]) -> List[Dict]:
        today = datetime.utcnow().day
        actual_load_hashes = {}
        outdated_products = []
        last_load_products_log = IBProductsLoadUtil.__get_last_load(ib_api_key)

        for product in products:
            internal_code = product["internal_code"]
            product_hash = hashlib.sha256(str(product).encode()).hexdigest()

            actual_load_hashes[internal_code] = {
                "day": today,
                "hash": product_hash,
            }

            if (
                internal_code not in last_load_products_log
                or last_load_products_log[internal_code]["hash"] != product_hash
                or last_load_products_log[internal_code]["day"] != today
            ):
                outdated_products.append(product)

        IBProductsLoadUtil.__save_load(ib_api_key, actual_load_hashes)
        return outdated_products

    @staticmethod
    def __get_last_load(ib_api_key: str) -> Dict:
        cache_file_path = IBProductsLoadUtil.__get_file_path(ib_api_key)
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, "r") as products_file:
                products_hash = json.load(products_file)["products"]
                return products_hash

        return {}

    @staticmethod
    def __save_load(ib_api_key: str, products_hash_update: Dict):
        cache_file_path = IBProductsLoadUtil.__get_file_path(ib_api_key)
        with open(cache_file_path, "w") as products_load_file:
            json.dump(
                {
                    "started_at": datetime.utcnow().isoformat(),
                    "products": products_hash_update,
                },
                products_load_file,
            )

    @staticmethod
    def __get_file_path(
        ib_api_key: str,
    ) -> str:
        if not os.path.exists(config.ib_integration_temp_files):
            os.makedirs(config.ib_integration_temp_files, exist_ok=True)

        return os.path.join(
            config.ib_integration_temp_files,
            f"ib{hashlib.sha256(ib_api_key.encode()).hexdigest()}.json",
        )
