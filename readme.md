# URL Shortener

Простой сервис для сокращения ссылок на Python 3.12 + FastAPI + SQLite.

## Установка и запуск

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
```

3. Установите проект и зависимости:
```bash
pip install .
```
*Если планируете запускать тесты:* `pip install ".[test]"`

4. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.
Интерактивная документация (Swagger): `http://127.0.0.1:8000/docs`.

## Тестирование
Для запуска тестов выполните:
```bash
pytest
```
```
def caesar_encrypt(text, shift):
    """
    Шифрование текста шифром Цезаря
    text: исходный текст на английском
    shift: величина сдвига (целое число)
    """
    result = ""
    
    for char in text:
        if char.isalpha():  # Проверяем, является ли символ буквой
            # Определяем базовый код (A=65, a=97)
            base = ord('A') if char.isupper() else ord('a')
            # Шифруем символ
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            # Небуквенные символы (пробелы, знаки препинания и т.д.) оставляем без изменений
            result += char
    
    return result

def main():
    print("=" * 50)
    print("Шифр Цезаря - Шифрование текста")
    print("=" * 50)
    
    # Ввод открытого текста
    plain_text = input("Введите открытый текст на английском языке: ")
    
    # Ввод сдвига с проверкой
    while True:
        try:
            shift = int(input("Введите величину сдвига (целое число): "))
            break
        except ValueError:
            print("Ошибка! Пожалуйста, введите целое число.")
    
    # Шифрование
    encrypted_text = caesar_encrypt(plain_text, shift)
    
    # Вывод результатов
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ШИФРОВАНИЯ:")
    print("=" * 50)
    print(f"Открытый текст:  {plain_text}")
    print(f"Сдвиг (n):       {shift}")
    print(f"Зашифрованный текст: {encrypted_text}")
    print("=" * 50)
    
    # Дополнительная информация
    if shift < 0:
        print(f"\nПримечание: Отрицательный сдвиг {shift} эквивалентен сдвигу влево на {abs(shift)} позиций.")
    elif shift > 25:
        print(f"\nПримечание: Сдвиг {shift} эквивалентен сдвигу на {shift % 26} (по модулю 26).")

if __name__ == "__main__":
    main()
```
