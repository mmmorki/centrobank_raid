from currency_parser import CurrencyParser

def main():
    print("=== Конвертер валют ЦБ РФ ===")
    print("Загрузка курсов валют...")
    
    # Создаем парсер
    parser = CurrencyParser()
    
    try:
        # Получаем актуальные курсы
        rates, last_update = parser.get_rates_from_cbr()
        print(f"Курсы обновлены: {last_update.strftime('%d.%m.%Y')}")
        print(f"Доступно валют: {len(rates)}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Используются резервные курсы (могут быть устаревшими)")
        # Можно добавить резервные курсы на случай ошибки
        return
    
    while True:
        try:
            print("\n" + "="*40)
            
            # Ввод суммы
            amount_input = input("Сумма: ").strip()
            if not amount_input:
                print("Сумма не может быть пустой")
                continue
                
            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("Сумма должна быть положительной")
                    continue
            except ValueError:
                print("Некорректная сумма. Используйте числа (например: 100 или 50.5)")
                continue
            
            # Ввод исходной валюты
            from_currency = input("Из валюты (код, например USD, EUR, RUB): ").strip().upper()
            if from_currency not in rates:
                print(f"Валюта {from_currency} не найдена. Доступные валюты: {', '.join(sorted(rates.keys())[:10])}...")
                continue
            
            # Ввод целевой валюты
            to_currency = input("В валюту (код): ").strip().upper()
            if to_currency not in rates:
                print(f"Валюта {to_currency} не найдена. Доступные валюты: {', '.join(sorted(rates.keys())[:10])}...")
                continue
            
            # Конвертация
            result = parser.convert_currency(amount, from_currency, to_currency)
            
            # Вывод результата
            print(f"\nРезультат: {amount:.2f} {from_currency} = {result:.2f} {to_currency}")
            
        except Exception as e:
            print(f"Ошибка: {e}")
            continue
        
        # Запрос на продолжение
        continue_choice = input("\nПродолжить конвертацию? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', 'д', 'да']:
            print("До свидания!")
            break

if __name__ == "__main__":
    main()