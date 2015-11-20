import django
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader_tags import BlockNode
from django.template.loader import get_template


def send_mail(template_name, context, from_email, recipient_list, fail_silently=False):
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
    body = body.render(context).strip('\r\n')
    if html:
        html = html.render(context).strip('\r\n')

    msg = EmailMultiAlternatives(subject, body, from_email, recipient_list)
    if html:
        msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=fail_silently)
