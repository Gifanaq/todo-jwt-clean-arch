# TODO JWT Clean Architecture

Учебный TODO-сервис: пользователи регистрируются и входят по логину/паролю,
а CRUD операций доступен только владельцу задач. Backend построен слоями
с Ports & Adapters; frontend находится в отдельном каталоге и подключается
к API через CORS.

## Backend: локальный запуск

Требуются Python 3.13, Poetry и Docker с Compose.

1. Создать локальный конфиг из шаблона:

   ```powershell
   Copy-Item backend\.env.example backend\.env
   ```

2. Заменить `ACCESS_SECRET` и `REFRESH_SECRET` на разные случайные значения
   длиной не менее 32 символов. Например, сгенерировать их через Python:

   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. Из корня репозитория установить зависимости и запустить PostgreSQL:

   ```powershell
   make backend-install
   make backend-db-up
   ```

4. Применить миграции и запустить API:

   ```powershell
   make backend-migrate
   make backend-run
   ```

   Swagger UI доступен по адресу `http://localhost:8000/docs`. По завершении
   работы остановить локальную БД: `make backend-db-down`.

Для разработки cookie использует `COOKIE_SECURE=false`. При публикации по HTTPS
установить `COOKIE_SECURE=true` и задать точный frontend origin в `CORS_ORIGINS`.
Не использовать примерные секреты из `.env.example` вне локальной разработки.

## API

- `POST /auth/register`, `POST /auth/login` — создают сессию и возвращают access token;
  refresh token устанавливается только в HttpOnly cookie.
- `POST /auth/refresh` — проверяет refresh cookie, отзывает предъявленный токен
  и выдает новую пару токенов.
- `POST /auth/logout` — отзывает текущую refresh-сессию и очищает cookie.
- `GET /auth/me` — возвращает идентификатор и логин из access token.
- `GET|POST /todos`, `PATCH|DELETE /todos/{id}` — CRUD задач владельца.

Access token передается как `Authorization: Bearer <token>`. Для refresh cookie
браузерный клиент должен отправлять запросы с credentials. Todo-запросы всегда
ограничивают выборку парой `todo_id` и `user_id` из проверенного access token;
чужие и отсутствующие задачи отвечают `404`.

## Архитектура

- `domain/` — сущности и порты репозиториев/безопасности.
- `application/` — auth и todo use cases, схемы API.
- `infrastructure/` — SQLAlchemy, PostgreSQL-репозитории, PBKDF2-SHA256 и JWT.
- `presentation/` — FastAPI роутеры, `Depends` и обработчики ошибок.
- `core/` — настройки, доменные ошибки и композиция адаптеров.

Пароли хэшируются через Passlib с `pbkdf2_sha256`; refresh JWT хранятся в БД
только как SHA-256-хэши. Для каждого входа создается отдельная refresh-сессия.
Refresh-токены ротируются в транзакции; access JWT подписываются отдельным
секретом и содержат тип токена, который проверяется при декодировании.

## Проверки

```powershell
make backend-test
make backend-lint
make backend-mypy
```