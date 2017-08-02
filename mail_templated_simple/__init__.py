import django
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import Context
from django.template.loader_tags import BlockNode
from django.template.loader import get_template


def email_message(template_name, context, *message_args, **message_kwargs):
    """Construct an email message from a template. The template is passed
    `context` as template context.

    The template is expected to contain ``{% block subject %}`` and
    ``{% block body %}``.  In addition, an HTML-formatted body may be added by
    the use of a ``{% block html %}``.  Both subject and body default to `None`
    if absent.

    :rtype: ``EmailMultiAlternatives``
    """
    template = get_template(template_name)

    if django.VERSION >= (1, 8):
        nodelist = template.template.nodelist
    else:
        nodelist = template.nodelist

    subject = body = html = None
    for block in nodelist:
        if isinstance(block, BlockNode):
            if block.name == 'subject':
                subject = block
            if block.name == 'body':
                body = block
            if block.name == 'html':
                html = block

    context = Context(context)

    if django.VERSION >= (1, 8):
        context.template = template.template

    subject = subject.render(context).strip('\r\n')
    assert subject is not None, "'subject' block is mandatory (but may be empty)"
    assert body is not None or html is not None, "One of 'html' or 'body' is mandatory (but may be empty)"

    if body:
        body = body.render(context).strip('\r\n')
    if html:
        html = html.render(context).strip('\r\n')

    if body and html:
        mail = EmailMultiAlternatives(subject, body, *message_args, **message_kwargs)
        mail.attach_alternative(html, 'text/html')
    elif body:
        mail = EmailMultiAlternatives(subject, body, *message_args, **message_kwargs)
    else:
        mail = EmailMultiAlternatives(subject, html, *message_args, **message_kwargs)
        mail.content_subtype = 'html'
    return mail


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
