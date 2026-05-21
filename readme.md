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
import random
import time
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

def heapsort(arr):
    """Пирамидальная сортировка (Heapsort)"""
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)
    # Построение max-кучи
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    # Извлечение элементов
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)
    return arr

def measure_time_and_sort(data, sort_func, name):
    """Измеряет время сортировки и возвращает отсортированный массив и время"""
    arr_copy = data.copy()
    start_time = time.perf_counter()
    sorted_arr = sort_func(arr_copy)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return sorted_arr, duration

def generate_reverse_sorted(arr):
    """Генерирует 'отсортированный наоборот' массив (по убыванию)"""
    return sorted(arr, reverse=True)

def write_to_excel(filename, original_data, reverse_data, sorted_original, time_original, sorted_reverse, time_reverse):
    """Записывает данные в Excel-файл"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Сортировки"

    # Заголовки
    headers = [
        "Исходный массив (случайные)",
        f"Пирамидальная сортировка\n(время: {time_original:.6f} с)",
        "Исходный массив (обратно отсортированный)",
        f"Пирамидальная сортировка\n(время: {time_reverse:.6f} с)"
    ]

    # Устанавливаем заголовки жирным шрифтом и выравнивание по центру
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Записываем данные
    max_len = max(len(original_data), len(reverse_data), len(sorted_original), len(sorted_reverse))
    for i in range(max_len):
        row_num = i + 2
        if i < len(original_data):
            ws.cell(row=row_num, column=1, value=original_data[i])
        if i < len(sorted_original):
            ws.cell(row=row_num, column=2, value=sorted_original[i])
        if i < len(reverse_data):
            ws.cell(row=row_num, column=3, value=reverse_data[i])
        if i < len(sorted_reverse):
            ws.cell(row=row_num, column=4, value=sorted_reverse[i])

    # Автоподбор ширины столбцов
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 20)
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(filename)
    print(f"Результаты сохранены в файл: {filename}")

def main():
    # Параметры
    SIZE = 50  # Размер массива (можно изменить)
    FILENAME = "sorting_results.xlsx"

    print(f"Генерация массивов (размер = {SIZE})...")

    # 1. Строго случайные данные
    random_data = [random.randint(1, 1000) for _ in range(SIZE)]

    # 2. "Отсортированные наоборот" случайные данные
    reverse_sorted_data = generate_reverse_sorted(random_data.copy())

    print("Сортировка случайного массива пирамидальной сортировкой...")
    sorted_random, time_random = measure_time_and_sort(random_data, heapsort, "Heapsort")

    print("Сортировка обратно отсортированного массива пирамидальной сортировкой...")
    sorted_reverse, time_reverse = measure_time_and_sort(reverse_sorted_data, heapsort, "Heapsort")

    print(f"Время сортировки случайных данных: {time_random:.6f} секунд")
    print(f"Время сортировки обратно отсортированных данных: {time_reverse:.6f} секунд")

    # Запись в Excel
    write_to_excel(FILENAME, random_data, reverse_sorted_data, 
                   sorted_random, time_random, 
                   sorted_reverse, time_reverse)

    # Демонстрация первых 10 элементов
    print("\nПример результатов (первые 10 элементов):")
    print(f"Случайные:          {random_data[:10]}")
    print(f"Отсортированные:    {sorted_random[:10]}")
    print(f"Обратно сортир.:    {reverse_sorted_data[:10]}")
    print(f"Отсортированные (обр.): {sorted_reverse[:10]}")

if __name__ == "__main__":
    main()
```
