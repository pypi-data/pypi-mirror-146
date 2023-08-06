import datetime
import os
import re
import time
import unicodedata
from dateutil import tz
from unidecode import unidecode


class IBUtil:

    @staticmethod
    def remove_special_characters(content: str) -> str:
        content = unidecode(content)
        string = re.sub(r'[^A-Za-z0-9]+', ' ', content)
        string = "".join(
            (
                c
                for c in unicodedata.normalize("NFD", string)
                if unicodedata.category(c) != "Mn"
            )
        )
        string = string.encode("latin-1", "ignore").decode("latin-1")
        return string

    @staticmethod
    def force_greater_or_equal_0(number) -> float:
        if number is None:
            number = 0.0
        if isinstance(number, str):
            number = number.replace(',', '.')

        try:
            number = float(number)
        except Exception:
            number = 0.0

        return max(number, 0.0)

    @staticmethod
    def get_payment_id(payment_method: str, erp_payments_option: dict) -> str:
        for erp_payments_option in erp_payments_option:
            if payment_method == erp_payments_option['ib_method'] or (
                    '_credit' in payment_method and '_credit' in erp_payments_option['ib_method']):
                return erp_payments_option['erp_id']

        raise Exception('Payment method ID not found.')

    @staticmethod
    def get_client_phone_number(phone: str, ddd=False) -> str:
        if ddd:
            return phone.split(')')[0].replace('(', '')
        else:
            return IBUtil.get_only_numbers_from_string(phone.split(')')[1])

    @staticmethod
    def format_value(value: float, decimal=2) -> str:
        if decimal == 2:
            value = '{:.2f}'.format(value)
        elif decimal == 4:
            value = '{:.4f}'.format(value)
        return ''.join('{:0>13}'.format(str(value)))

    @staticmethod
    def complete_empty_positions(string, size, append_size='right', character=' ') -> str:
        if not string:
            string = ''
        else:
            string = str(string)

        string = string[:size]

        if append_size == 'left':
            return character * (size - len(string)) + string
        else:
            return string + character * (size - len(string))

    @staticmethod
    def date_from_iso_string(date_string: str, force_end_of_day=False) -> datetime:
        if 'Z' in date_string:
            date_string = date_string.replace('Z', '+00:00')
        if len(date_string) == 24:
            date_string = date_string[:-2] + ':' + date_string[-2:]

        date = datetime.datetime.fromisoformat(date_string)
        if not date.tzinfo:
            date = date.astimezone(tz=tz.tzrange(-3))

        if len(date_string) == 10 and force_end_of_day:
            date = date + datetime.timedelta(days=1, seconds=-1)

        date = date.replace(tzinfo=None)

        return date

    @staticmethod
    def check_if_file_is_being_uploaded(file_path):
        while True:
            file_size = os.path.getsize(file_path)
            time.sleep(10)
            if os.path.getsize(file_path) == file_size:
                return

    @staticmethod
    def pop_keys(dic, keys):
        for key in keys:
            if key in dic:
                dic.pop(key)

    @staticmethod
    def string_to_datetime(date_string, force_end_of_day=False) -> datetime:
        date = datetime.datetime.strptime(date_string, '%d/%m/%Y')
        if force_end_of_day:
            date = date.replace(hour=23, minute=59, second=59)
        else:
            date = date.replace(hour=0, minute=0, second=0)

        return date

    @staticmethod
    def get_only_numbers_from_string(string) -> str:
        if not string:
            string = ''
        else:
            string = str(string)

        return ''.join([n for n in string if n.isdigit()])

    @staticmethod
    def remove_folder_or_file(path):
        try:
            os.remove(path)
        except Exception:
            pass

        try:
            os.rmdir(path)
        except Exception:
            pass
