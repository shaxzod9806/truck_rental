# CRM

integration of CRM with belting rezina
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirments.

```bash
pip install -r requirements.txt
```

## Env variables
Change below variables to connect database (PostgreSQL)

```python
# Database name
DB_NAME = motochas
# Database User
DB_USER = postgres
# Database Password
DB_PASSWORD = password
# Database host
DB_HOST = localhost
# Database port
DB_PORT = 5432
# Debug option(For Development process put True, for production level put False)
DEBUG = True
```

## To create table in database run below commands
``` 
python manage.py makemigrations
```

``` 
python manage.py migrate
```

## To create superuser in Django run below commands
```
python manage.py createsuperuser
```



## For questions and feedbacks:
phone: +99894 612 84 84 

telegram: [@AbdurazzoqovAbdulla](http://t.me/AbdurazzoqovAbdulla)