import django
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string


def email_message(template_name, context, *message_args, **message_kwargs):
    """Construct an email message from a template. The template is passed
    `context` as template context.

    The template is expected to contain ``{% block subject %}`` and
    ``{% block body %}``.  In addition, an HTML-formatted body may be added by
    the use of a ``{% block html %}``.  Both subject and body default to `None`
    if absent.

    :rtype: ``EmailMultiAlternatives``
    """
    template = render_to_string(template_name, context)

    subject = _find_block(template, 'subject')
    body = _find_block(template, 'body')
    html = _find_block(template, 'html')
    assert subject is not None, "'subject' block is mandatory (but may be empty)"
    assert body is not None or html is not None, "One of 'html' or 'body' is mandatory (but may be empty)"

    if body and html:
        mail = EmailMultiAlternatives(subject, body, *message_args, **message_kwargs)
        mail.attach_alternative(html, 'text/html')
    elif body:
        mail = EmailMultiAlternatives(subject, body, *message_args, **message_kwargs)
    else:
        mail = EmailMultiAlternatives(subject, html, *message_args, **message_kwargs)
        mail.content_subtype = 'html'
    return mail


def _find_block(template, tag):
    start_tag = '###___%s___###' % tag
    end_tag = '###___end%s___###' % tag
    start_tag_idx = template.find(start_tag)
    end_tag_idx = template.find(end_tag)
    assert start_tag_idx != -1 and end_tag_idx != -1, 'Could not find %s tag. Did you include {% extends "mail_templated_simple/base.tpl" %} in your template?'
    return template[start_tag_idx+len(start_tag):end_tag_idx]


def send_mail(template_name, context, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    """This is what :func:`django.core.mail.send_mail` is for normal messages.

    Note that instead of the `subject` and `message` parameters this convience
    function expects a `template_name` and `context` from which subject and
    message are derived.
    """
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    mail = email_message(template_name, context, from_email, recipient_list,
                         connection=connection)
    return mail.send()


def send_mass_mail(template_name, datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    """This is what :func:`django.core.mail.send_mass_mail` is for normal messages.

    Note that the layout of `datatuple` is different from Django's.
    It is expected to be in this format::

        (context, from_email, recipient_list)
    """
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    messages = [email_message(template_name, context, sender, recipient,
                             connection=connection)
                for context, sender, recipient in datatuple]
    return connection.send_messages(messages)
