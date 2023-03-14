import json
import requests
from config import keys


class ConvertionExeption(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        amount = amount.replace(',', '.')

        if quote == base:
            raise ConvertionExeption(f'Невозможно перевести одинаковые валюты {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать количество {amount}')

        if amount < 0:
            raise ConvertionExeption(f'Для ввода доступны только положительные числа')


        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {base}')

        a = requests.get(
            f"https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=601509d7031a099d159f1f55a7ce70e4").text
        total_base = json.loads(a)['data'][keys[quote] + keys[base]]

        return total_base