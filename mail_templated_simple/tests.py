from django.test import TestCase
from django.core import mail
from mail_templated_simple import send_mail


class Tests(TestCase):
    def test_full_example(self):
        ctx = {'foo': "Foo"}
        from_email = 'from@example.com'
        recipient_list = ['to@example.com', 'to2@example2.com']
        send_mail("mail_templated_simple/test_data/full_example.tpl", ctx, from_email, recipient_list)

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, recipient_list)
        self.assertEqual(msg.from_email, from_email)
        self.assertEqual(msg.subject, "Example subject, Foo")
        self.assertEqual(msg.body, "Example plaintext, Foo")
        self.assertEqual(len(msg.alternatives), 1)
        self.assertEqual(msg.alternatives[0], ("Example html, Foo", "text/html"))


    def test_without_html(self):
        send_mail("mail_templated_simple/test_data/plaintext_only_example.tpl", None, None, ['to@example.org'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(mail.outbox[0].alternatives)
        self.assertEqual(mail.outbox[0].body, "Only plaintext body")
