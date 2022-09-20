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
