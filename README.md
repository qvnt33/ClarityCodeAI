# **Clarity Code AI**

Це **автоматизований інструмент для перевірки кодових завдань**, побудований на основі **FastAPI**.
Проєкт інтегрується з **GitHub API** для отримання репозиторіїв та використовує **OpenAI GPT API** для аналізу коду.

Мета — автоматизувати процес рецензування коду, включаючи пошук недоліків, оцінювання якості коду та надання висновків.


## **Функціонал**

- Отримання файлів із заданого репозиторію через **GitHub API**.
- Аналіз коду за допомогою **OpenAI GPT API** (GPT-4o).
- Генерація висновків:
	- Недоліки.
	- Оцінка (0–10).
	- Загальний висновок.
- Кешування відповідей за допомогою **Redis**.
- Використання **Docker** для розгортання проєкту.

## Інструкція з налаштуванняx

### 1. Клонування репозиторію
```
git clone https://github.com/qvnt33/ClarityCodeAI.git
cd clarity-code-ai
```

### 2. Створення віртуального середовища
```
python -m venv .venv
source .venv/bin/activate  # Для Linux/MacOS
```

або

```
.\.venv\Scripts\activate  # Для Windows
```

### 3. Встановлення залежностей

```
pip install -r requirements.txt
```

### 4. Налаштування середовища

1. У головній директорії знайдіть файл `.env.example`.
2. Створіть копію цього файлу та назвіть її `.env`.
3. Додайте до `.env` ваші ключі API та параметри **Redis**:
	- `OPENAI_API_KEY=<your_openai_api_key>`
	- `GITHUB_TOKEN=<your_github_token>`
	- `REDIS_HOST=localhost` (*Локально*)
	- `REDIS_HOST=redis` (*Docker*)
	- `REDIS_PORT=6379`

## Запуск проєкту (локально)

### Запуск FastAPI

```
uvicorn app.main:app --reload
```
Сервер буде доступний за адресою: `http://127.0.0.1:8000/`.

## Запуск проєкту (Docker)

### Запуск Docker Compose
```
docker-compose up --build
```
Сервер буде доступний за адресою: `http://127.0.0.1:8000/`.


## API Ендпоінти

### POST /review-assignment

**Опис:**
Аналізує репозиторій **GitHub** і генерує висновки щодо якості коду.

**Приклад запиту:**

```
{
    "assignment_description": "Write an expense management API with Django REST Framework",
    "github_repo_url": "https://github.com/octocat/Hello-World",
    "candidate_level": "Junior"
}
```

**Приклад відповіді:**

```
{
    "downsides_comments": "1. No code provided for review.\n2. Lack of any implementation details in the provided code snippet.\n3. The file appears to contain unrelated content to a Django REST Framework implementation.",
    "rating": "1/10",
    "conclusion": "The provided code snippet lacks any relevant content for review as it only contains a simple \"Hello World!\" message. For a Junior developer level, this is inadequate as it does not demonstrate any coding skills related to building an expense management API using Django REST Framework. Additional code related to the assignment would be necessary to evaluate the developer's proficiency in this area.",
    "file_list": "- README"
}
```

## Тестування
Для запуску тестів використовуйте **pytest**:

```
pytest --cov=app
```

## Масштабування

### Виклики

1.	100+ запитів на хвилину.
2.	Робота з великими репозиторіями (>100 файлів).

### Рішення

1. Обробка великого навантаження:
	- Використовувати **Celery** для обробки запитів у фоновому режимі.
	- Зберігати результати в **Redis** для повторного доступу без перерахунку.
2. Великі репозиторії:
	- Завантажувати з **GitHub** лише необхідні файли, щоб зменшити навантаження.
3.	OpenAI API:
	- Обʼєднувати менші файли перед відправленням.
	- Використовувати кешування, щоб уникнути повторної обробки тих самих даних.
4. Інфраструктура:
	- Запускати систему у **Docker** для простого масштабування.
5.	Економія ресурсів:
	- Зменшити кількість зайвих запитів до **OpenAI** і **GitHub API**.
	- Оптимізувати код для швидкої обробки.
