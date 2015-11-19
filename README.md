django-mail-templated-simple
============================

I did this reimplementation of [django-mail-templated](https://github.com/artemrizhov/django-mail-templated) because it was causing problems with
[django-celery-email](https://github.com/pmclanahan/django-celery-email).

In this version, `mail_templated.send_mail` is simply a wrapper around Django's `send_mail`.

Django >= 1.8 is required, although Django < 1.8 support is easy to obtain by reverting some minor changes. See commit history.
