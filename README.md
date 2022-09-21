## Usage
You can test app on page <b>185.180.231.142:8000</b>
or send direct request:
```sh
curl -X GET http://185.180.231.142:8000/item/{id}
```

## Setup

Clone repository:

```sh
$ git clone https://github.com/bridges123/stripe_task.git
$ cd stripe_task
```

Create a virtual environment:

```sh
$ python -m venv venv
$ source vevn/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

After downloading dependencies you can run server:
```sh
(env)$ python manage.py runserver
```

Or to direct request:
```sh
curl -X GET http://localhost:8000/item/{id}
```

To use Order functionality need to log-in in admin panel (for start):
<a>http://185.180.231.142:8000/admin</a> with login/pass - admin:admin
