# dcms

A work-in-progress Django content management system for building pages, blogs, and forums.

## Features
* REST API
* posts and Reddit-like comments
* tagging and categorizing contents
* images/media files uploading
* pages with different layouts

## Requirements

```
Python >=3.6, Django 2.1, Django Rest Framework 3.8.2
```

## Installing
```
# creating a new virtual environment and installing the dependencies.
[sudo] pip install virtualenv
virtualenv venv
cd venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Tests
```
cd dcms
python manage.py test
```

## To-dos
* documentation
* more unit tests
* filtering objects in query
* use Django template engine to render posts
* search, i18n, apps
    * page: use_hyperlink option.
* permalink for content
* demo frontend
