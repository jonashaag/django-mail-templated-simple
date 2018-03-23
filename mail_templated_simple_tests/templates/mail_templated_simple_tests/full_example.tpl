{% extends "mail_templated_simple/base.tpl" %}
{% block subject %} Example subject, {{ foo }}
{% endblock %}
{% block body %}
Example plaintext, {{ foo }}
 {% endblock %}
{% block html %}Example html, {{ foo }}{% endblock %}
