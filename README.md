django-mail-templated-simple
============================

I did this reimplementation of [django-mail-templated](https://github.com/artemrizhov/django-mail-templated) because it was causing problems with
django-celery-email (currently maintained version here: https://github.com/DigiACTive/django-celery-email).

In this version, `mail_templated.send_mail` is simply a wrapper around Django's `send_mail`.
