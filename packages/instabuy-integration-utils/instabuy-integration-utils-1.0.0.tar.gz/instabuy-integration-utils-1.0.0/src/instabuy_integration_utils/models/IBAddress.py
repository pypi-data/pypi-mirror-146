class IBAddress:

    def __init__(self, address_dict: dict):
        self.zipcode: str = address_dict['zipcode']
        self.state: str = address_dict['state']
        self.city: str = address_dict['city']
        self.neighborhood: str = address_dict['neighborhood']
        self.street: str = address_dict['street']
        self.street_number: str = address_dict['street_number']
        self.complement: str = address_dict['complement']
        self.country: str = address_dict['country']
