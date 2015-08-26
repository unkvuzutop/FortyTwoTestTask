# -*- coding: utf-8 -*-
import json
from datetime import datetime
import os
from PIL import Image
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
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
        self.assertIn(getattr(request, 'path'), response.content)

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
                         json.dumps({'response': 'Nothing to update'}))

        self.client.get(reverse('hello:home'))

        test_request = RequestHistory.objects.latest('id')

        self.assertEqual(test_request.is_viewed, False)
        response = self.client.post(reverse('hello:ajax_update'),
                                    {'viewed': test_request.id},
                                    **self.kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps({'response': 'OK'}))

        test_request = RequestHistory.objects.get(pk=test_request.id)
        self.assertEqual(test_request.is_viewed, True)

        response = self.client.get(reverse('hello:ajax_update'))
        self.assertEqual(response.content, json.dumps({'response': 'False'}))

    def test_ajax_count_view(self):
        """
        make 15 test requests
        check requests count in DB
        check ajax response count is equal 10
        mark some request as viewed and check ajax response (count become 9
            but objects count still 10)
        check response if request not ajax request
        """
        test_requests_count = 15
        for request in range(0, 15):
            self.client.get(reverse('hello:requests'))

        response = self.client.post(reverse('hello:ajax_count'), {},
                                    **self.kwargs)

        response_data = json.loads(response.content)

        get_requests_count = RequestHistory.objects\
            .filter(is_viewed=False)\
            .count()

        self.assertEqual(get_requests_count, test_requests_count)
        self.assertEqual(response_data['count'], 10)

        last_request = RequestHistory.objects.latest('id')
        RequestHistory.objects.filter(id=last_request.id)\
            .update(is_viewed=True)

        response = self.client.post(reverse('hello:ajax_count'), {},
                                    **self.kwargs)
        response_data = json.loads(response.content)

        self.assertEqual(response_data['count'], 9)
        self.assertEqual(len(response_data['requests']), 10)

        response = self.client.get(reverse('hello:ajax_count'))

        self.assertEqual(response.content, json.dumps({'response': 'False'}))

    def test_ten_latest_requests_on_page(self):
        """
        make eleven requests and check:
            - check the first request is not on template context
            - check latest  (10) request on template context and their data
                on the page
        """
        self.client.get(reverse('hello:home'))
        for request in range(1, 10):
            self.client.get(reverse('hello:requests'))
        response = self.client.get(reverse('hello:requests'))

        for request in response.context['latest_requests']:
            self.assertEqual(reverse('hello:requests'), request.path)
        self.assertIn(reverse('hello:requests'), response.content)

    def test_ten_latest_request_from_ajax(self):
        """
        make eleven requests and check:
            - check the first request  is not on the response
            - check latest  (10) request in the response
        """
        self.client.get(reverse('hello:home'))
        for request in range(0, 10):
            self.client.get(reverse('hello:requests'))
        response = self.client.post(reverse('hello:ajax_count'), {},
                                    **self.kwargs)
        response_data = json.loads(response.content)

        for request in response_data['requests']:
            self.assertEqual(reverse('hello:requests'), request['path'])

class EditPageTests(TestCase):
    def setUp(self):
            self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def auth_user(self):
        self.client.login(username='admin', password='admin')

    def test_edit_page_access(self):
        """
        1) check login required for edit page
        2) check page is available after login
        """
        response = self.client.get(reverse('hello:user_edit'))
        self.assertEqual(response.status_code, 302)

        self.auth_user()

        response = self.client.get(reverse('hello:user_edit'))
        self.assertEqual(response.status_code, 200)

    def test_update_form(self):
        """
        1) check response after update form
        2) check response if request in not Ajax
        3) check response if one of required fields is empty in update request
        4) check response if form not valid
        """
        self.auth_user()
        test_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
        form_data = dict(name='name', last_name='last name',
                         date_of_birth=test_date,
                         bio='some Bio', email=settings.ADMIN_EMAIL,
                         jabber=' test jabber', skype='test skype',
                         other_contacts='my other contacts')

        response = self.client.post(reverse('hello:user_edit'),
                                    form_data, **self.kwargs)

        self.assertEqual(response.status_code, 200)

        self.assertIn('name', response.content)
        self.assertIn('last name', response.content)
        self.assertIn(test_date,
                      response.content)
        self.assertIn('some Bio', response.content)
        self.assertIn('test jabber', response.content)
        self.assertIn('test skype', response.content)
        self.assertIn('my other contacts', response.content)

        self.assertNotIn('This field is required.', response.content)
        self.assertNotIn('Enter a valid', response.content)

        response = self.client.post(reverse('hello:user_edit'),
                                    form_data)

        self.assertEqual(response.status_code, 302)

        form_data.pop('email')
        response = self.client.post(reverse('hello:user_edit'),
                                    form_data, **self.kwargs)
        self.assertEqual(response.status_code, 400)
        self.assertIn('This field is required.', response.content)
        self.assertIn('email', response.content)

        form_data['date_of_birth'] = '0000-00-00'
        response = self.client.post(reverse('hello:user_edit'),
                                    form_data, **self.kwargs)
        self.assertIn('This field is required.', response.content)
        self.assertIn('date_of_birth', response.content)

    def test_two_object_in_db(self):
        """
        check right data on edit page if 2 users in database
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

        self.auth_user()

        response = self.client.get(reverse('hello:user_edit'))

        self.assertIn('Сергей', response.content)
        self.assertIn('Благун', response.content)
        self.assertIn('sergey.drower@gmail.com', response.content)
        self.assertIn('unkvuzutop@khavr.com', response.content)
        self.assertIn('unkvuzutop', response.content)
        self.assertIn('some additional info', response.content)
        self.assertIn('my other contacts', response.content)
        self.assertIn('1987-04-04', response.content)

        self.assertNotIn('Сергій', response.context)
        self.assertNotIn('Благун', response.context)
        self.assertNotIn('інша біографія', response.context)
        self.assertNotIn('sergey.other@gmail.com', response.context)
        self.assertNotIn('unkvuzutop@khavr.com', response.context)
        self.assertNotIn('unkvuzutop1', response.context)
        self.assertNotIn('1999-08-08', response.context)
        self.assertNotIn('other contacts', response.context)

    def test_edit_page_with_unicode(self):
        """
        test edit page with unicode data
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

        self.auth_user()

        response = self.client.get(reverse('hello:user_edit'))
        self.assertIn('Сергій', response.content)
        self.assertIn('Благун', response.content)
        self.assertIn('sergey.drower@gmail.com', response.content)
        self.assertIn('unkvuzutop@khavr.com', response.content)
        self.assertIn('unkvuzutop', response.content)
        self.assertIn('інша біографія', response.content)
        self.assertIn('other contacts', response.content)
        self.assertIn('1999-08-08', response.content)

    def test_edit_page_with_empty_user(self):
        """
        check edit page if user doesn't exist
        """
        Profile.objects.all().delete()
        self.auth_user()
        response = self.client.get(reverse('hello:user_edit'))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Page Not Found', response.content)

    def test_image(self):
        """
        check image saving and checking whether generated previews
        """
        profile = Profile.objects.get(email=getattr(settings,
                                                    'ADMIN_EMAIL'))

        image = Image.open(StringIO(os.path.join(
            getattr(settings, 'BASE_DIR'), 'assets', 'img', 'test_img.jpg'))
            .read())

        output = StringIO()
        image.save(output, format='JPEG', quality=75)

        output.seek(0)
        profile.photo = InMemoryUploadedFile(output,
                                             None,
                                             'test.jpg',
                                             'image/jpeg',
                                             output.len,
                                             None)
        profile.save()
        profile = Profile.objects.get(email=getattr(settings,
                                                    'ADMIN_EMAIL'))

        self.assertTrue(profile.photo_preview.width <= 200)
        self.assertTrue(profile.photo_preview.height <= 200)

        self.assertTrue(profile.photo_preview.path)
        self.assertTrue(profile.photo.path)
