from datetime import datetime
import json
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase


from apps.hello.models import User, RequestHistory
from apps.hello.templatetags.admin_tags import admin_url
from fortytwo_test_task import settings


class HomePageTests(TestCase):
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


class RequestsPageTests(TestCase):
    def setUp(self):
        self.request_object = RequestHistory.\
            objects.create(path='/',
                           host='127.0.0.1',
                           method='GET',
                           ip='127.0.0.1',
                           date='2015-01-01 00:00:01',
                           is_viewed=0)
        self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_requests_page_is_work(self):
        """
        check status of requests page
        and check this last request in the page context
        """
        response = self.client.get(reverse('hello:requests'))
        self.assertEqual(response.status_code, 200)

        request = RequestHistory.objects.latest('id')
        requests_count = RequestHistory.objects.count()
        self.assertEqual(len(response.context['latest_requests']),
                         requests_count)
        self.assertEqual(request.id, response.context['last_request'].id)

    def test_data_on_page(self):
        """
        make some requests and check:
            - check all of that requests in DB
            - check count of objects in the template context
        """
        requests_before = RequestHistory.objects.count()

        urls = ['home', 'requests']
        requests_factor = 5
        test_requests_count = len(urls)*requests_factor

        for url in requests_factor * urls:
            self.client.get(reverse('hello:'+url))

        requests_after = RequestHistory.objects.count()
        self.assertEqual(requests_after-requests_before, test_requests_count)

        response = self.client.get(reverse('hello:requests'))
        self.assertLessEqual(len(response.context['latest_requests']),
                             test_requests_count)

    def test_ajax_update_view(self):
        """
        check update ajax request:
        - check response if request with not real object ID
        - check response if request with real object ID
        - check object is_viewed state before and after request
        - check response with not ajax request
        """
        response = self.client.post(reverse('hello:ajax_update'),
                                    {'viewed': 0}, **self.kwargs)
        self.assertEqual(response.content,
                         '{"response": "Nothing to update"}')

        test_request = RequestHistory.objects.latest('id')

        self.assertEqual(test_request.is_viewed, False)
        response = self.client.post(reverse('hello:ajax_update'),
                                    {'viewed': test_request.id},
                                    **self.kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"response": "OK"}')

        test_request = RequestHistory.objects.get(pk=test_request.id)
        self.assertEqual(test_request.is_viewed, True)

        response = self.client.get(reverse('hello:ajax_update'))
        self.assertEqual(response.content, '{"response": "False"}')

    def test_ajax_count_view(self):
        """
        check real count of new request
        check last request in response is real last response
        check response if request not ajax request
        """
        response = self.client.post(reverse('hello:ajax_count'),
                                    {'last_loaded_id': 0},
                                    **self.kwargs)
        response_data = json.loads(response.content)

        get_requests_count = RequestHistory.objects.count()
        get_lastes_request = RequestHistory.objects.latest('id')
        self.assertEqual(response_data['count'], get_requests_count)
        self.assertEqual(response_data['last_request'], get_lastes_request.id)

        response = self.client.get(reverse('hello:ajax_count'))

        self.assertEqual(response.content, '{"response": "False"}')


class EditPageTests(TestCase):
    def setUp(self):
            self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_edit_page_access(self):
        """
        1) check login required for edit page
        2) check page is available after login
        3) check response after update form
        4) check response if request in not Ajax
        5) check response if one from required fields
            doesn't given in form_data
        """
        response = self.client.get(reverse('hello:user_edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')

        response = self.client.get(reverse('hello:user_edit'))
        self.assertEqual(response.status_code, 200)

        form_data = dict(name='name', last_name='last name',
                         date_of_birth=datetime.strftime(datetime.now(),
                                                         '%Y-%m-%d'),
                         bio='some Bio', email=settings.ADMIN_EMAIL,
                         jabber='jabber', skype='skype',
                         other_contacts='other contacts')

        response = self.client.post(reverse('hello:user_edit'),
                                    form_data, **self.kwargs)

        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('hello:user_edit'),
                                    form_data)

        self.assertEqual(response.status_code, 302)

        form_data.pop('email')
        response = self.client.post(reverse('hello:user_edit'),
                                    form_data, **self.kwargs)
        self.assertEqual(response.status_code, 400)


class TemplateTagTest(TestCase):
    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def test_tag(self):
        """
        render template for template tag and compare
        result from template and result from tag method
        """
        user = User.objects.get(email=settings.ADMIN_EMAIL)

        tag_template = self.render_template(
            '{% load admin_tags %}{% admin_url user %}',
            context={'user': user})

        self.assertEqual(tag_template, admin_url(user))
