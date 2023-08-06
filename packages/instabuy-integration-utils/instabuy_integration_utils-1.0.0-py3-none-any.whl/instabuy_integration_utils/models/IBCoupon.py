class IBCoupon:

    def __init__(self, coupon_dict: dict):
        self.coupon_type: str = coupon_dict['coupon_type']
        self.discount_value: float = coupon_dict['discount_value']
