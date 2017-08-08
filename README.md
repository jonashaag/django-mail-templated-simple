[![Build Status](https://travis-ci.org/jonashaag/django-mail-templated-simple.svg?branch=master)](https://travis-ci.org/jonashaag/django-mail-templated-simple) [![codecov.io](https://codecov.io/github/jonashaag/django-mail-templated-simple/coverage.svg?branch=master)](https://codecov.io/github/jonashaag/django-mail-templated-simple?branch=master)

# django-mail-templated-simple

I did this reimplementation of [django-mail-templated](https://github.com/artemrizhov/django-mail-templated) because it was causing problems with
[django-celery-email](https://github.com/pmclanahan/django-celery-email) (see [#7](https://github.com/artemrizhov/django-mail-templated/issues/7), [#8](https://github.com/artemrizhov/django-mail-templated/issues/8)).

In this version, `mail_templated.send_mail` is simply a wrapper around Django's `send_mail`.

Compatible with:

- Python 2.7, 3.4, 3.5, 3.6
- Django 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11

## Usage

**Note:** Breaking change in version 3. You must now have your templates extend a base template, as follows:

```django
{% extends "mail_templated_simple/base.tpl" %}

{% block subject %}Example subject, {{ foo }}{% endblock %}

{% block body %}
Example plaintext, {{ foo }}
{% endblock %}

{% block html %}
<p>
  Example html, {{ bar }}
</p>
{% endblock %}
```

At least one of plaintext ``body`` and ``html`` is mandatory. ``subject`` is always mandatory.
