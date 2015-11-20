django-mail-templated-simple
============================

I did this reimplementation of [django-mail-templated](https://github.com/artemrizhov/django-mail-templated) because it was causing problems with
[django-celery-email](https://github.com/pmclanahan/django-celery-email) (see [#7](https://github.com/artemrizhov/django-mail-templated/issues/7), [#8](https://github.com/artemrizhov/django-mail-templated/issues/8)).

In this version, `mail_templated.send_mail` is simply a wrapper around Django's `send_mail`.

Python >= 2.6 and Django >= 1.4 are tested, but other versions may also work. Patches welcome (if required).
