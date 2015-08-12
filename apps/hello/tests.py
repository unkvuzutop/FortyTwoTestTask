# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from django.conf import settings
from apps.hello.models import Profile, RequestHistory


class PersonalPageTests(TestCase):
    def test_email_in_settings(self):
        """
        check ADMIN_EMAIL is present in settings and it's not empty
        """
        self.assertTrue(getattr(settings, 'ADMIN_EMAIL'))
        self.assertEqual(settings.ADMIN_EMAIL, 'sergey.drower@gmail.com')

    def test_user_with_email(self):
        """
        check user with ADMIN_EMAIL is unique
        """
        user = Profile.objects.filter(email=settings.ADMIN_EMAIL).count()
        self.assertEqual(user, 1)

    def test_home_view(self):
        """
        check access for home page
        check user  info in template context
        """
        response = self.client.get(reverse('hello:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/user_detail.html')

        self.assertIn('Сергей', response.content)
        self.assertIn('Благун', response.content)
        self.assertIn('sergey.drower@gmail.com', response.content)
        self.assertIn('unkvuzutop@khavr.com', response.content)
        self.assertIn('unkvuzutop', response.content)
        self.assertIn('some additional info', response.content)
        self.assertIn('my other contacts', response.content)
        self.assertIn('04-04-1987', response.content)

    def test_home_with_unicode(self):
        """
        test home page with unicode data
        """
        Profile.objects.all().delete()
        Profile.objects.create(name=u'Сергій',
                               last_name=u'Благун',
                               bio=u'інша біографія',
                               email=u'sergey.drower@gmail.com',
                               jabber=u'unkvuzutop@khavr.com',
                               skype=u'unkvuzutop',
                               date_of_birth=u'1999-08-08',
                               other_contacts=u'other contacts')

        response = self.client.get(reverse('hello:home'))
        self.assertIn('Сергій', response.content)
        self.assertIn('Благун', response.content)
        self.assertIn('sergey.drower@gmail.com', response.content)
        self.assertIn('unkvuzutop@khavr.com', response.content)
        self.assertIn('unkvuzutop', response.content)
        self.assertIn('інша біографія', response.content)
        self.assertIn('other contacts', response.content)
        self.assertIn('08-08-1999', response.content)

    def test_home_page_with_empty_user(self):
        """
        check home page if user doesn't exist
        """
        Profile.objects.all().delete()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page Not Found', response.content)

    def test_two_object_in_db(self):
        """
        check right data on home page if 2 users in database
        """
        Profile.objects.create(name=u'Сергій',
                               last_name=u'Благун',
                               bio=u'інша біографія',
                               email=u'sergey.other@gmail.com',
                               jabber=u'unkvuzutop@khavr.com',
                               skype=u'unkvuzutop1',
                               date_of_birth=u'1999-08-08',
                               other_contacts=u'other contacts')

        users = Profile.objects.count()
        self.assertGreaterEqual(users, 2)

        response = self.client.get(reverse('hello:home'))
        self.assertIn('Сергей', response.content)
        self.assertIn('Благун', response.content)
        self.assertIn('sergey.drower@gmail.com', response.content)
        self.assertIn('unkvuzutop@khavr.com', response.content)
        self.assertIn('unkvuzutop', response.content)
        self.assertIn('some additional info', response.content)
        self.assertIn('my other contacts', response.content)
        self.assertIn('04-04-1987', response.content)

        self.assertNotIn('Сергій', response.context)
        self.assertNotIn('Благун', response.context)
        self.assertNotIn('інша біографія', response.context)
        self.assertNotIn('sergey.other@gmail.com', response.context)
        self.assertNotIn('unkvuzutop@khavr.com', response.context)
        self.assertNotIn('unkvuzutop1', response.context)
        self.assertNotIn('1999-08-08', response.context)
        self.assertNotIn('other contacts', response.context)


class RequestsPageTests(TestCase):
    def setUp(self):
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

    def test_right_data_on_page(self):
        """
        - make some unique request and check it on request page
        """
        test_url = '/sometesturl/'
        self.client.get(test_url)
        response = self.client.get(reverse('hello:requests'))
        self.assertIn(test_url, response.content)

    def test_no_requests_in_db(self):
        """
        check request page while RequestHistory is empty
        """
        RequestHistory.objects.all().delete()
        response = self.client.get(reverse('hello:requests'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('/requests', response.content)
        self.assertEqual(len(response.context['latest_requests']), 1)

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
