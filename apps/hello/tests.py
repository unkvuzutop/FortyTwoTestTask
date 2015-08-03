from django.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
from apps.hello.models import User
from fortytwo_test_task import settings


class TemplateTests(TestCase):
    def test_email_in_settings(self):
        """
        check ADMIN_EMAIL is present in settings and it's not empty
        """
        self.assertIn('ADMIN_EMAIL', settings.__dict__)
        self.assertNotEqual(settings.ADMIN_EMAIL, '')

    def test_user_with_email(self):
        """
        check user with ADMIN_EMAIL is unique
        """
        user = User.objects.filter(email=settings.ADMIN_EMAIL).count()
        self.assertEqual(user, 1)
        self.assertNotEqual(user, 0)

    def test_home_view(self):
        """
        check access for home page
        """
        response = self.client.get(reverse('hello:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/user_detail.html')

    def test_personal_info(self):
        """
        check personal info in DB  and data structure
        """
        user = User.objects.filter(email=settings.ADMIN_EMAIL).first()
        self.assertIsNotNone(user)

        self.assertIn('name', user.__dict__)
        self.assertIn('last_name', user.__dict__)
        self.assertIn('date_of_birth', user.__dict__)
        self.assertIn('bio', user.__dict__)
        self.assertIn('jabber', user.__dict__)
        self.assertIn('skype', user.__dict__)
        self.assertIn('other_contacts', user.__dict__)
