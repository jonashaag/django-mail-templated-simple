from setuptools import setup

setup(
    name         = "django-mail-templated-simple",
    author       = "Jonas Haag",
    author_email = "jonas@lophus.org",
    license      = "ISC",
    url          = "https://github.com/jonashaag/mail_templated_simple",
    description  = 'A simple reimplementation of "django-mail-templated"',
    version      = "1.0",

    packages = ['mail_templated_simple'],
    zip_safe = False,
    include_package_data = True,

    classifiers = ['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: ISC License',
                   'Framework :: Django',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5' ],
)