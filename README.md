# Image Analyzer

Простой инструмент для анализа и трансформации изображений, извлечения базовых признаков и сохранения результатов в базу данных.

## Суть проекта

- Загружает изображения по переданному пути.
- Применяет трансформации к изображениям(изменение размера, яркости, контраста или применение фильтра: размытость, 
  резкость, усиление границ, поиск границ).
- Извлекает базовые признаки(яркость, контраст, плотность границ).
- Сохраняет результаты анализа и историю изменений в базу данных.
- Визуализирует модифицированные данные(сравнение до/после и гистограмма изображения).

## Структура проекта
```
image-analyzer/
├── src/
│   ├── core/              # Логика анализа и обработки изображений
│   ├── models/            # Модели данных
│   └── database/          # Работа с SQLite 
│ 
├── tests/                 # Автоматические тесты
├── data/                  # Директория для изображений
├── main.py                # Точка входа CLI-приложения
├── pyproject.toml         # Конфигурация Poetry
├── README.md              # Документация
└── .gitignore
```

## Установка и запуск
### Клонирование репозитория
```
git clone https://github.com/logunova-anastasia/image_analyzer.git
cd image_analyzer
```

### Создание виртуального окружения
```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv/Scripts/activate  # Windows
```

### Установка зависимостей
```
poetry install
```

### Запуск программы
```
poetry run python main.py
```

## Пример работы
```
Enter the path to the image: data/sample1.jpg
Choose the transformstion regime:
  - Resize
  - Brightness
  - Contrast
  - Filter
Enter the regime: resize
Enter the width (px): 800
Enter the height (px): 600
Enter the name for the new file: new_sample1
All done!
```

<img alt="img.png" src=".\data\comparison.jpg"/>