# dcms

A work-in-progress Django content management system for building small websites, blogs, and forums.

## Features
* REST API
* posts and Reddit-like comments
* tagging and categorizing contents

### Requirements

```
Python 3.6.5, Django 2.0.5, Django Rest Framework 3.8.2
```

## To-dos
* unit test for each app
* documentation
* filtering objects in query
* use Django template engine to render posts
* page, search, i18n, vote apps
    * page: a page consists of (component, queryset) pairs. Allows user to set use_hyperlinked_serializer.
* permalink for content
* demo website and admin frontend
* use Django sites framework
