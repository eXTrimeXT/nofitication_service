# Notification Service
Django-сервис для отправки уведомлений пользователям через различные каналы связи с обеспечением надежной доставки.

## Возможности
- Многоканальная отправка: Telegram, Email, SMS.
- Надежная доставка: Автоматическое переключение между каналами при сбоях
- Приоритет отправки: Telegram → Email → SMS (SMS платные, частично)
- Админ-панель: Удобное управление уведомлениями и пользователями
- Статусы отправки: Отслеживание статуса каждого уведомления

## Требования
- Python 3.12.6
- Django 5.2.6
- Почта Gmail
- Аккаунт на https://smsaero.ru/ (50 рублей при регистрации)

## Установка
```
git clone https://github.com/eXTrimeXT/nofitication_service.git
cd ./nofitication_service
python -m venv .venv
```
#### Активация окружения
Windows 

```
.venv\Scripts\activate
``` 

Linux/Mac 
``` 
source .venv/bin/activate
```

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Настройка сервисов отправки
1. Telegram Bot
- Создайте бота через @BotFather
- Получите токен бота
- Добавьте токен в TELEGRAM_BOT_TOKEN
- Пользователь должен начать диалог с ботом командой /start
2. Email (Gmail)
- Включите двухфакторную аутентификацию
- Создайте пароль приложения
- Используйте его в EMAIL_PSWD
- Подробнее тут https://habr.com/ru/articles/675130/
3. SMS (https://smsaero.ru/)
- Зарегистрируйтесь на SMSAero
- Получите API ключ в личном кабинете 
- Настройте подпись отправителя

## Настройки конфигурации
Откройте файл notifications/config.py

Заполните поля
- SMSAERO_EMAIL - ваш email при регистрации
- SMSAERO_API_KEY - API ключ в настройках

![sms_aero_api](https://github.com/eXTrimeXT/nofitication_service/blob/main/assets/images/sms_aero_api.png)

- SMTP_HOST = "82.2"
- SMTP_PORT = 27

![sms_aero_api_1](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/sms_aero_api_1.png)

- Создайте аккаунт для SMPP-доступа

![sms_aero_api_2](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/sms_aero_api_2.png)

- В качестве IP-адреса нужно указать свой.
- SMTP_LOGIN = "smtp"
- SMTP_PSWD = "ваш_пароль"

## Использование
```
python manage.py runserver
```

Админ-панель доступна по адресу: http://127.0.0.1:8000/admin/

## Работа с админ-панелью
Пользователи и контакты:

Создайте пользователей в разделе "Authentication and Authorization" → "Users"

Добавьте контактные данные в разделе "Notifications" → "Контакты пользователей"

![ap_1](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/ap_1.png)

Создание уведомлений:

Перейдите в раздел "Notifications" → "Уведомления"

Нажмите "Добавить уведомление"

Выберите пользователя и введите текст сообщения

![ap_2](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/ap_2.png)


Отправка уведомлений:

В списке уведомлений выберите нужные записи

Используйте действие "Отправить выбранные уведомления" и нажмите кнопку "Go"

Система автоматически попробует все доступные каналы связи

![ap_3](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/ap_3.png)



## Алгоритм отправки
Сервис использует следующий порядок отправки:
- Telegram (приоритетный канал)
- Требуется: telegram_chat_id в контактах пользователя

При сбое переходит к следующему каналу
- Email (резервный канал)
- Требуется: email в контактах пользователя

Использует SMTP для отправки
- SMS (последний резерв)
- Требуется: phone в контактах пользователя
- Пробует три метода отправки: API → SMTP → SMPP

## Модели данных
### Notification
- user - пользователь-получатель
- message - текст уведомления 
- status - статус отправки (pending/sent/failed)
- created_at - дата создания 
- sent_at - дата успешной отправки
- UserContact
- user - связь с пользователем
- telegram_chat_id - ID чата в Telegram
- email - email адрес
- phone - номер телефона

## На заметку
СМС-сообщение отправляется с задержкой на модерацию.

![sms_aero](https://github.com/eXTrimeXT/nofitication_service/blob/main/asserts/images/sms_aero.png)


## Разработка
Структура проекта
```
notification_service/
├── notifications/              # Приложение Django 
│   ├── models.py               # Модели данных
│   ├── admin.py                # Настройки админки
│   ├── config.py               # Конфигурация
│   ├── signals.py              # Сигналы Django
│   └── senders.py              # Сервисы отправки
│       ├── EmailSender.py      # Отправитель Email
│       ├── SMSSender.py        # Отправитель SMS
│       └── TelegramSender.py   # Отправитель Telegram
├── notification_service/       # Проект Django
│   ├── settings.py             # Настройки Django
│   └── urls.py                 # URL-маршруты
├── manage.py                   # Утилита управления
└── requirements.txt            # Зависимости Python
```
