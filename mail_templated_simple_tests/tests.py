from django.test import TestCase
from django.core import mail
import mail_templated_simple


class Tests(TestCase):
    def test_full_example(self):
        ctx = {'foo': "Foo"}
        from_email = 'from@example.com'
        recipient_list = ['to@example.com', 'to2@example2.com']
        mail_templated_simple.send_mail(
            "mail_templated_simple_tests/full_example.tpl",
            ctx, from_email, recipient_list,
        )

        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, recipient_list)
        self.assertEqual(msg.from_email, from_email)
        self.assertEqual(msg.subject, "Example subject, Foo")
        self.assertEqual(msg.body, "Example plaintext, Foo")
        self.assertEqual(len(msg.alternatives), 1)
        self.assertEqual(msg.alternatives[0], ("Example html, Foo", "text/html"))

    def test_without_html(self):
        mail_templated_simple.send_mail(
            "mail_templated_simple_tests/plaintext_only_example.tpl",
            {'foo': '<script>'}, None, ["to@example.com"],
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].body, "Only plaintext body <script>")

    def test_without_body(self):
        mail_templated_simple.send_mail(
            "mail_templated_simple_tests/html_only_example.tpl",
            {'foo': '<script>'}, None, ["to@example.com"],
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].content_subtype, 'html')
        self.assertEqual(mail.outbox[0].body, "Only HTML body &lt;script&gt;")

    def test_email_message(self):
        msg = mail_templated_simple.email_message(
            "mail_templated_simple_tests/plaintext_only_example.tpl",
            {}, cc=["cc@cc.cc"],
        )
        self.assertEqual(msg.cc, ["cc@cc.cc"])

    def test_send_mass_mail(self):
        recipient_list1 = ["to@example.com", "to2@example.com"]
        recipient_list2 = ["to3@example.com"]
        from_email1 = "from1@example.com"
        from_email2 = "from2@example.com"

        mail_templated_simple.send_mass_mail(
            "mail_templated_simple_tests/full_example.tpl",
            [({'foo': "Test 1"}, from_email1, recipient_list1),
             ({'foo': "Test 2"}, from_email2, recipient_list2)],
        )

        self.assertEqual(len(mail.outbox), 2)
        msg1 = mail.outbox[0]
        self.assertEqual(msg1.to, recipient_list1)
        self.assertEqual(msg1.from_email, from_email1)
        self.assertEqual(msg1.subject, "Example subject, Test 1")
        msg2 = mail.outbox[1]
        self.assertEqual(msg2.to, recipient_list2)
        self.assertEqual(msg2.from_email, from_email2)
        self.assertEqual(msg2.subject, "Example subject, Test 2")
