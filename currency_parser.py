import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime



class CurrencyParser:
    def __init__(self):
        self.rates = {}
        self.last_update = None
    
    def get_rates_from_cbr(self):
        """
        Получает курсы валют с сайта ЦБ РФ
        Возвращает словарь с курсами в формате {код_валюты: курс}
        """
        try:
            # URL API ЦБ РФ в XML формате (более стабильный, чем парсинг HTML)
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            
            # Парсим XML
            root = ET.fromstring(response.content)
            # Извлекаем дату обновления
            date_str = root.attrib['Date']
            self.last_update = datetime.strptime(date_str, "%d.%m.%Y")
            
            # Извлекаем курсы валют
            self.rates = {'RUB': 1.0}  # RUB всегда 1
            
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                value = float(valute.find('Value').text.replace(',', '.'))
                nominal = int(valute.find('Nominal').text)
                
                # Рассчитываем курс за 1 единицу валюты
                rate = value / nominal
                self.rates[char_code] = rate
            
            return self.rates, self.last_update
            
        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении данных: {e}")
        except ET.ParseError as e:
            raise Exception(f"Ошибка при разборе данных: {e}")
        except Exception as e:
            raise Exception(f"Неожиданная ошибка: {e}")
    
    def get_available_currencies(self):
        """Возвращает список доступных валют"""
        return list(self.rates.keys())
    
    def convert_currency(self, amount, from_currency, to_currency):
        """
        Конвертирует сумму из одной валюты в другую
        """
        try:
            if from_currency not in self.rates:
                raise ValueError(f"Валюта {from_currency} не найдена")
            if to_currency not in self.rates:
                raise ValueError(f"Валюта {to_currency} не найдена")
            
            # Конвертация через RUB как базовую валюту
            amount_in_rub = amount * self.rates[from_currency]
            result = amount_in_rub / self.rates[to_currency]
            
            return round(result, 2)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Ошибка при конвертации: {e}")