<div align="center">

# TODO JWT

### Ваш список дел — только ваш. Ваша сессия — всегда под контролем.

Полноценное full-stack приложение для персональных задач: зарегистрируйтесь,
соберите свой список и возвращайтесь к нему в любое время.

<br />

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/UI-React-149ECA?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)

</div>

---


## Задачи — без лишнего шума

Создавайте дела, отмечайте выполненные, редактируйте список и быстро находите
нужное с помощью фильтров. Приложение хранит задачи раздельно для каждого
аккаунта и восстанавливает сессию после обновления страницы или закрытия браузера.

### Что умеет приложение

- **Персональные списки:** пользователь видит и меняет только собственные задачи.
- **Полный цикл задачи:** создание, редактирование, завершение и удаление.
- **Удобный обзор:** фильтры «Все», «Активные» и «Выполненные», счётчик
  незавершённых дел.
- **Сессия переживает F5:** access-токен хранится в памяти приложения, а
  refresh-токен — в `HttpOnly` cookie.
- **Автоматическое продление:** frontend обновляет access-токен и повторяет
  запрос при истечении сессии.
- **Чистое разделение ответственности:** API, application-сервисы, домен и
  инфраструктура не смешаны в одном слое.

## Технологии

| Часть | Стек |
|---|---|
| Backend | Python 3.13, FastAPI, Pydantic, Pydantic Settings |
| Доступ к данным | SQLAlchemy 2, Alembic, PostgreSQL |
| Аутентификация | PyJWT (HS256), PBKDF2-SHA256 через Passlib |
| Frontend | React, TypeScript, Vite, Axios |
| Локальная база | Docker Compose |

## Запуск локально

Нужны Python 3.13, Poetry, Node.js/npm и Docker Compose. Команды ниже приведены
для Bash. Если GNU Make установлен, используйте короткие команды из
`Makefile` — запускайте их из корня репозитория. Доступные цели можно посмотреть
через `make help`. Backend, frontend и Docker запускаются в отдельных
терминалах.

### 1. Создайте локальные настройки

Из корня репозитория скопируйте шаблоны, если локальные `.env` ещё не созданы:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

В `backend/.env` укажите **два разных случайных секрета**, каждый не короче
32 символов. Сгенерируйте секрет командой и выполните её дважды:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Выберите, к какой PostgreSQL будет подключаться приложение:

- **Docker Compose:** Compose публикует контейнерный порт `5432` на порт
  компьютера `5432`, поэтому задайте в `backend/.env`:
  `DATABASE_URL=postgresql+psycopg://todo:todo@localhost:5433/todo_db`.
- **Установленный локальный PostgreSQL:** оставьте или укажите свой URL и порт,
  например `localhost:5432`, а также соответствующие имя базы и учётные данные.

Шаблон backend `.env.example` по умолчанию использует `5432` для локального
PostgreSQL.

### 2. Установите зависимости, запустите БД и примените миграции

Рекомендуемый способ — цели `Makefile` из корня проекта:

```bash
make backend-install
make backend-db-up
```

Проверьте `docker compose ps` и дождитесь `healthy`, затем примените миграции:

```bash
make backend-migrate
```

`backend-install` устанавливает Python-зависимости через Poetry,
`backend-db-up` запускает PostgreSQL в Compose, а `backend-migrate` применяет
миграции. Дождитесь состояния `healthy` у контейнера базы перед миграцией.
Если используете установленный PostgreSQL, пропустите `backend-db-up` и
убедитесь, что ваша БД запущена.

Без Make те же действия можно выполнить напрямую:

```bash
docker compose up -d db
cd backend
poetry install
poetry run alembic upgrade head
cd ..
```

> Если используете Docker, сначала запустите БД (`make backend-db-up` или
> `docker compose up -d db`), затем примените миграцию. `upgrade head`
> применяет существующие миграции и создаёт таблицы в пустой базе; запуск
> приложения сам по себе миграции не создаёт и не применяет.

Дополнительная проверка текущей ревизии и соответствия моделей:

```bash
cd backend
poetry run alembic current
poetry run alembic check
cd ..
```

### 3. Запустите backend

В отдельном терминале из корня проекта:

```bash
make backend-run
```

Либо без Make из каталога `backend`:

```bash
cd backend
poetry run uvicorn src.main:app --reload
```

API: <http://localhost:8000> · Swagger UI: <http://localhost:8000/docs>

### 4. Установите и запустите frontend

В отдельном терминале из корня проекта:

```bash
make frontend-install
make frontend-run
```

Без Make команды из каталога `frontend`:

```bash
cd frontend
npm ci
npm run dev -- --port 3000 --strictPort
```

Откройте приложение: <http://localhost:3000>. Адрес API задаётся через
`VITE_API_URL` в `frontend/.env`. Для браузерных запросов backend разрешает
origin `http://localhost:3000`; если измените порт frontend, обновите
`CORS_ORIGINS` в `backend/.env` и перезапустите API.

### Остановка

Остановите frontend и API сочетанием `Ctrl+C`. Контейнер Compose остановите
из корня проекта:

```bash
docker compose down
```

Команда сохраняет данные в Docker volume. Чтобы удалить volume вместе со всеми
локальными данными базы, используйте `docker compose down -v`.

## Попробуйте приложение

1. Зарегистрируйтесь: логин и пароль от **8** символов.
2. Добавьте несколько задач и отметьте одну выполненной.
3. Переключите фильтры и отредактируйте название задачи.
4. Обновите страницу: активная сессия должна восстановиться автоматически.
5. Выйдите, войдите под другим пользователем и убедитесь, что список задач
   изолирован.

Для ручного знакомства с API откройте Swagger UI на
<http://localhost:8000/docs>.

## API

| Метод | Путь | Назначение | Требует |
|---|---|---|---|
| `POST` | `/auth/register` | Регистрация и новая сессия | — |
| `POST` | `/auth/login` | Вход и новая сессия | — |
| `POST` | `/auth/refresh` | Ротация refresh-токена | HttpOnly cookie |
| `POST` | `/auth/logout` | Отзыв текущей сессии | HttpOnly cookie |
| `GET` | `/auth/me` | Данные пользователя из access JWT | Bearer token |
| `GET` | `/todos` | Список задач пользователя | Bearer token |
| `POST` | `/todos` | Создать задачу | Bearer token |
| `PATCH` | `/todos/{id}` | Изменить название или статус | Bearer token |
| `DELETE` | `/todos/{id}` | Удалить задачу | Bearer token |

Access-токен передаётся в заголовке `Authorization: Bearer <token>`.
Несуществующая и чужая задача одинаково отвечают `404`, не раскрывая другому
пользователю наличие записи.

## Как устроен проект

```text
backend/src/
├── domain/          # сущности и порты репозиториев и безопасности
├── application/     # AuthService и TodoService
├── infrastructure/  # SQLAlchemy, PostgreSQL, JWT и хэширование паролей
├── presentation/    # FastAPI routes, dependencies и API-схемы
└── core/            # конфигурация, доменные ошибки и композиция

frontend/src/
├── api/             # HTTP-клиент, auth и todo-запросы
├── auth/            # состояние пользователя и восстановление сессии
├── components/      # переиспользуемые компоненты интерфейса
└── pages/           # экран входа и список задач
```

Зависимости backend направлены внутрь: `presentation → application → domain`,
`infrastructure → domain`. Composition root связывает сервисы с адаптерами
через FastAPI `Depends`. Frontend использует Axios-интерцепторы для Bearer
авторизации и обновления истёкшего access-токена.

## Аутентификация: ключевые решения

- Пароли хэшируются `pbkdf2_sha256`; исходный пароль не сохраняется.
- Для access и refresh JWT используются разные HS256-секреты и TTL:
  **15 минут** и **30 дней**.
- Claim `type` проверяется при декодировании, поэтому refresh-токен нельзя
  предъявить вместо access-токена.
- Access JWT находится в памяти frontend; refresh JWT устанавливается как
  `HttpOnly` cookie с путём `/auth`.
- В базе хранится SHA-256-хэш refresh-токена, а не сам токен.
- Refresh-ротация отзывает предъявленный токен и создаёт новый в одной
  транзакции. Несколько устройств/входов могут иметь отдельные сессии.
- `COOKIE_SECURE=false` предназначен только для локального HTTP. Для HTTPS
  окружения задайте `COOKIE_SECURE=true` и точный список CORS origins.

## Проверки и миграции

### Backend

Из корня репозитория при установленном GNU Make:

```bash
make backend-test
make backend-lint
make backend-mypy
```

Или напрямую из каталога `backend`:

```bash
cd backend
poetry run pytest
poetry run ruff check src tests migrations
poetry run mypy src
```

Backend-тесты используют SQLite in-memory и покрывают JWT, регистрацию и вход,
refresh/logout, отклонение неверного типа токена и изоляцию задач пользователей.
Для проверки PostgreSQL отдельно примените миграции и пройдите сценарий в
запущенном API.

### Frontend

Makefile запускает frontend-проверки из корня проекта:

```bash
make frontend-lint
make frontend-build
```

Или напрямую из `frontend`:

```bash
npm run lint
npm run build
```

`frontend-build` выполняет проверку TypeScript и production-сборку Vite.
Frontend unit-test runner пока не настроен.

### Изменение схемы базы

После изменения SQLAlchemy-модели создайте миграцию, проверьте сгенерированный
файл, затем примените его:

```bash
cd backend
poetry run alembic revision --autogenerate -m "краткое описание"
poetry run alembic upgrade head
```

Autogenerate сравнивает метаданные моделей с текущей БД и создаёт файл миграции;
он не обновляет базу автоматически. Просмотрите миграцию перед применением.
