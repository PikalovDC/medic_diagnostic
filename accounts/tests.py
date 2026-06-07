from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from appointments.models import Appointment, Doctor
from services.models import Service, ServiceCategory

User = get_user_model()


class AccountsModelTests(TestCase):
    """Тесты для модели пользователя"""

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
            first_name='Test',
            last_name='User',
            phone='+79991234567',
            is_patient=True
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_patient)
        self.assertFalse(user.is_doctor)
        self.assertEqual(str(user), 'Test User (testuser)')

    def test_create_doctor_user(self):
        user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='pass123',
            is_doctor=True,
            is_patient=False
        )
        self.assertTrue(user.is_doctor)
        self.assertFalse(user.is_patient)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class AccountsRegistrationTests(TestCase):
    """Тесты регистрации"""

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '+79998887766',
            'birth_date': '1990-01-01',
        }

    def test_register_page_accessible(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')

    def test_register_duplicate_username(self):
        User.objects.create_user(username='newuser', password='pass')
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Form error, no redirect
        self.assertEqual(User.objects.count(), 1)  # No new user created


class AccountsAuthorizationTests(TestCase):
    """Тесты авторизации"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!',
            email='test@example.com'
        )
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.logout_url = reverse('logout')

    def test_login_page_accessible(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'StrongPass123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.profile_url}')

    def test_profile_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_logout(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout_redirects_home(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_appointment_history_requires_login(self):
        response = self.client.get(reverse('appointment_history'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("appointment_history")}')

    def test_appointment_history_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='StrongPass123!')
        response = self.client.get(reverse('appointment_history'))
        self.assertEqual(response.status_code, 200)