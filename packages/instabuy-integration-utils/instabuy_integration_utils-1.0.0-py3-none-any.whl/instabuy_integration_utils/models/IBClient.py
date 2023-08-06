import datetime
from instabuy_integration_utils.utils.IBUtil import IBUtil


class IBClient:
    def __init__(self, client_dict: dict):
        self.user_type: str = client_dict["user_type"]
        self.email: str = (
            client_dict["email"] if client_dict.get("email") else "sem@email.com"
        )
        self.phone: str = client_dict["phone"]
        self.id: str = client_dict["id"]
        self.created_at: datetime = IBUtil.date_from_iso_string(
            client_dict["created_at"]
        )

        if self.is_pf():
            self.first_name: str = client_dict["first_name"]
            self.last_name: str = client_dict["last_name"]
            self.cpf: str = client_dict["cpf"]
            self.birthday: datetime = IBUtil.date_from_iso_string(
                client_dict["birthday"]
            )
            self.gender: str = client_dict["gender"]
        else:
            self.company_name: str = client_dict["company_name"]
            self.fantasy_name: str = client_dict["fantasy_name"]
            self.cnpj: str = client_dict["cnpj"]

    def is_pf(self) -> bool:
        return self.user_type == "PF"

    def get_document(self) -> str:
        return IBUtil.get_only_numbers_from_string(
            self.cpf if self.is_pf() else self.cnpj
        )

    def get_complete_name(self) -> str:
        if self.is_pf():
            return f"{self.first_name} {self.last_name}"

        return self.fantasy_name
