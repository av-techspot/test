# Email Domain Validator

Проверка доменов email через DNS-записи MX.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

Через аргументы:

```bash
python email_validator.py -e test@example.com user@gmail.com
```

Из файла (по одному email в строке):

```bash
python email_validator.py -f emails.txt
```

Необязательный параметр таймаута DNS-запроса:

```bash
python email_validator.py -e test@example.com --timeout 3
```

