import datetime
from typing import List
from .IBAddress import IBAddress
from .IBCheckoutOption import IBCheckoutOption
from .IBClient import IBClient
from .IBCoupon import IBCoupon
from .IBOrderProduct import IBOrderProduct
from instabuy_integration_utils.utils.IBUtil import IBUtil


class IBBuy:

    def __init__(self, buy_dict: dict):
        self.id: str = buy_dict["id"]
        self.created_at: datetime = IBUtil.date_from_iso_string(buy_dict["created_at"])
        self.subtotal: float = buy_dict["_subtotal"]
        self.freight: float = buy_dict["freight"]
        self.discount: float = buy_dict["_discount"]
        self.total: float = buy_dict["_total"]
        self.comment: str = buy_dict["comment"]
        self.code: str = buy_dict["code"]
        self.erp_id: int = buy_dict.get("erp_id")
        self.buy_type: str = buy_dict["buy_type"]
        self.was_paid: bool = buy_dict["_was_paid"]
        self._already_injected_delivery_tax_on_products_array = False

        self.client = IBClient(buy_dict["client"])

        if buy_dict.get("delivery_info"):
            self.delivery_info = IBAddress(buy_dict["delivery_info"])
        else:
            self.delivery_info = None

        if buy_dict.get("coupon"):
            self.coupon = IBCoupon(buy_dict["coupon"])
        else:
            self.coupon = None

        if buy_dict.get("checkout_option"):
            self.checkout_option = IBCheckoutOption(buy_dict["checkout_option"])
        else:
            self.checkout_option = None

        self.products: List[IBOrderProduct] = []
        # todo implement kits
        for prod_dict in buy_dict["products"]:
            if prod_dict["qtd"] > 0:
                self.products.append(IBOrderProduct(prod_dict))

        self.payment_method: str = buy_dict["payment_info"]["method"]
        self.payment_value: str = buy_dict["payment_info"].get("value")
        self.installments: int = (
            buy_dict["installment"]["installments_number"]
            if buy_dict.get("installment")
            else 1
        )

        if buy_dict.get("delivery_hour"):
            self.delivery_hour = buy_dict["delivery_hour"]
        else:
            self.delivery_hour = None

    def inject_delivery_tax_on_products_array(self, delivery_tax_internal_code):
        if not self._already_injected_delivery_tax_on_products_array:
            if self.freight > 0:
                delivery_tax_product = IBOrderProduct()
                delivery_tax_product.price = self.freight
                delivery_tax_product.qtd = 1.0
                delivery_tax_product.model_internal_code = delivery_tax_internal_code
                delivery_tax_product.name = "Taxa de Entrega"
                self.products.append(delivery_tax_product)
                self._already_injected_delivery_tax_on_products_array = True

            elif self.checkout_option and self.checkout_option.additional_price:
                checkout_option_product = IBOrderProduct()
                checkout_option_product.price = self.checkout_option.additional_price
                checkout_option_product.qtd = 1.0
                checkout_option_product.model_internal_code = delivery_tax_internal_code
                checkout_option_product.name = self.checkout_option.order_item_name
                self.products.append(checkout_option_product)
