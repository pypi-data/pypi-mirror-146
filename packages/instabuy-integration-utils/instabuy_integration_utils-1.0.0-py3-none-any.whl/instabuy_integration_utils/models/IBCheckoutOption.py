class IBCheckoutOption:
    def __init__(self, checkout_option_dict: dict):
        self.order_item_name = checkout_option_dict["order_item_name"]
        self.additional_price = checkout_option_dict["additional_price"]
