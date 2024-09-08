# user-auth-api-django-port


### **Задание для портфолио: Создание API для управления пользователями и аутентификацией на Django с использованием современных технологий**

#### **Цель проекта:**

Создать полноценное API для управления пользователями и аутентификацией с использованием Django и Django Rest Framework. Проект должен включать передовые технологии для обеспечения безопасности, контейнеризации, тестирования, автоматизации и удобства работы с API. Конечный результат должен быть продемонстрирован на GitHub с хорошей структурой и документацией.

### **Основной функционал API:**

1. **Регистрация пользователей**
   * Пользователь может зарегистрироваться, предоставив email и пароль.
   * Данные валидируются, и создается новая учетная запись.
2. **Авторизация пользователей с использованием JWT**
   * Пользователь может войти в систему и получить JWT токен.
   * Токен используется для аутентификации на защищенных эндпоинтах.
3. **Управление профилем пользователя**
   * Пользователь может просматривать и обновлять информацию своего профиля.
   * Включает такие данные, как имя, email, биография, аватар и местоположение.
4. **Смена пароля**
   * Пользователь может сменить свой пароль, введя текущий и новый пароли.
   * Предусмотрена валидация для защиты от атак.
5. **Защита эндпоинтов**
   * Эндпоинты для управления профилем и смены пароля защищены с использованием JWT токенов.

### **Технологии, которые будут использоваться:**

1. **Django & Django Rest Framework**
   * Основной фреймворк для разработки API.
2. **JWT (JSON Web Tokens)**
   * Для аутентификации пользователей с помощью библиотеки `djangorestframework-simplejwt`.
3. **Swagger / OpenAPI (drf-yasg)**
   * Для автоматической генерации и предоставления документации по API.
4. **CORS (django-cors-headers)**
   * Для поддержки междоменных запросов, если фронтенд хостится на другом домене.
5. **Celery + Redis**
   * Для обработки фоновых задач, таких как отправка уведомлений по электронной почте.
6. **Docker**
   * Контейнеризация приложения для создания предсказуемой среды разработки и деплоя.
7. **CI/CD (GitHub Actions)**
   * Автоматизация процессов тестирования и развертывания.
8. **Rate Limiting (django-ratelimit)**
   * Ограничение частоты запросов для защиты от злоупотреблений.
9. **Sentry**
   * Для мониторинга ошибок в реальном времени в продакшене.
