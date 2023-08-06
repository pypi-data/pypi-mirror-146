from typing import List


class IBOrderProduct:

    def __init__(self, product_dict: dict = None):
        if product_dict:
            self.id: str = product_dict['id']
            self.model_internal_code: str = product_dict['model_internal_code']
            self.name: str = product_dict['name']
            self.price: float = product_dict['price']
            self.qtd: float = product_dict['qtd']
            self.unit_type: str = product_dict['unit_type']
            self.bar_codes: List[str] = product_dict['bar_codes']
