from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MainPageTests(TestCase):

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'main/home.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contacts.html')

    def test_contacts_form_post_valid(self):
        response = self.client.post(reverse('contacts'), {
            'name': 'John',
            'email': 'john@example.com',
            'phone': '+79991234567',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_contacts_form_post_invalid(self):
        response = self.client.post(reverse('contacts'), {
            'name': '',
            'email': 'invalid',
            'message': ''
        })
        self.assertEqual(response.status_code, 200)  # Form error