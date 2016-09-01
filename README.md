# python-batian
Python agent for the Batian Application monitoring platform.
Currently only supports Django. More frameworks will be supported soon.

## Installation

### via pip
```
    $ pip install python batian
```

### via github (for development purposes)
```
    $ git clone git@github.com:ishuah/python-batian.git
    $ cd python-batian
    $ pip install -e .
```

## Usage

### Django
After installation, add two variables to your settings.py:
```
    BATIAN_APP_NAME = 'myapp'
    BATIAN_SERVER_URL = 'http://<mybatianserverdomainorport>:<port>/api/v1/event'
```

Then add batian to your INSTALLED_APPS
```
    INSTALLED_APPS = [
        ...
        'batian',
        ...
    ]
```

Finally, add the batian middleware to your MIDDLEWARE_CLASSES. Make sure it's the at the top of the list otherwise the agent won't be able to log everything.
```
    MIDDLEWARE_CLASSES = [
        'batian.contrib.django.middleware.BatianAPMMiddleware',
        ...
    ]
```