#!/usr/bin/env python

from setuptools import find_packages, setup

REQUIREMENTS = [
    "asgiref==3.2.7",
    "beautifulsoup4==4.9.0",
    "certifi==2020.4.5.1",
    "chardet==3.0.4",
    "defusedxml==0.6.0",
    "django-allauth-templates-bootstrap4==0.34.12",
    "django-allauth==0.41.0",
    "django-annoying==0.10.6",
    "django-appconf==1.0.4",
    "django-compressor==2.4",
    "django-crispy-forms==1.9.0",
    "django-environ==0.4.5",
    "django-filter==2.2.0",
    "django-jsonstore==0.4.1",
    "django-material==1.6.3",
    "django-model-utils==4.0.0",
    "django-viewflow==1.6.0",
    "django-prometheus==2.0.0",
    "Django==3.1.12",
    "idna==2.9",
    "invoke==1.4.1",
    "humanize==2.3.0",
    "Jinja2==2.11.1",
    "MarkupSafe==1.1.1",
    "matplotlib==3.2.1",
    "numpy==1.18.2",
    "oauthlib==3.1.0",
    "pandas==1.0.3",
    "psycopg2-binary==2.8.4",
    "python3-openid==3.1.0",
    "pytz==2019.3",
    "rcssmin==1.0.6",
    "requests-oauthlib==1.3.0",
    "requests==2.23.0",
    "rjsmin==1.1.0",
    "six==1.14.0",
    "soupsieve==2.0",
    "sqlparse==0.3.1",
    "urllib3==1.25.8",
    "django_select2==7.2.3",
]

DEV_REQUIREMENTS = [
    "black==19.10b0",
    "coverage==5.0.4",
    "django-debug-toolbar==2.2",
    "django-extensions==2.2.9",
    "faker==4.0.2",
    "pytest==5.4.1",
    "pytest-django==3.9.0",
    "pre-commit==2.2.0",
    "pycodestyle==2.5.0",
    "Werkzeug==1.0.1",
]

PROD_REQUIREMENTS = ["gunicorn==20.0.4"]

setup(
    name="Pydemic Hospital Capacity",
    version="0.0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
        "prod": PROD_REQUIREMENTS,
        "staging": DEV_REQUIREMENTS + PROD_REQUIREMENTS,
    },
    zip_safe=False,
    entry_points={"console_scripts": ["hcap = manage:main"]},
)
