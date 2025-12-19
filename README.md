# Image Analyzer

Простой инструмент для анализа и трансформации изображений, извлечения базовых признаков и сохранения результатов в JSON.  

---

## Суть проекта

- Загружает изображения с локального диска или по URL.
- Применяет трансформации к изображениям.
- Извлекает базовые признаки.
- Сохраняет результаты анализа и историю изменений в JSON.
- Визуализирует модифицированные данные.

---

## Структура проекта
```
image-analyzer/
├── src/
│   ├── core/              # Логика анализа и обработки изображений
│   ├── models/            # Модели данных
│   └── database/          # Работа с SQLite 
│ 
├── tests/
├── data/                  # Примеры изображений
├── main.py                # Точка входа CLI-приложения
├── pyproject.toml         # Конфигурация Poetry
├── README.md              # Документация
└── .gitignore
```
---
## Setup 
```
# Клонирование репозитория
git clone https://github.com/logunova-anastasia/image_analyzer.git
cd image_analyzer

# Установка зависимостей
poetry install

# Запуск программы
poetry run python main.py
```
---
## Example
```
Enter the path to the image: data/sample1.jpg
Choose the transformstion regime:
  - Resize
  - Brightness
  - Contrast
  - Filter
Enter the regime: filter
Enter the Filter (for example, 'blur', 'sharpen', 'edge_enhance', 'edges'): blur
Enter the name for the new file: new_sample1
All done!
```
---
# Good luck and have fun!