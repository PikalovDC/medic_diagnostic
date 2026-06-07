from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from services.models import Service, ServiceCategory
from appointments.models import Appointment, Doctor
from datetime import date, timedelta

User = get_user_model()


class AppointmentModelTests(TestCase):
    """Тесты для модели записей"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='patient',
            password='pass123',
            is_patient=True
        )
        self.category = ServiceCategory.objects.create(name='Diagnostics')
        self.service = Service.objects.create(
            name='MRI',
            category=self.category,
            price=5000,
            duration=60,
            description='MRI scan'
        )

    def test_create_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.user,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='pending'
        )
        self.assertEqual(appointment.patient, self.user)
        self.assertEqual(appointment.service, self.service)
        self.assertEqual(appointment.status, 'pending')
        self.assertEqual(str(appointment), f'{self.user.get_full_name()} - MRI ({date.today() + timedelta(days=1)})')

    def test_appointment_status_choices(self):
        appointment = Appointment.objects.create(
            patient=self.user,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='confirmed'
        )
        self.assertEqual(appointment.get_status_display(), 'Подтверждена')

    def test_appointment_ordering(self):
        Appointment.objects.create(
            patient=self.user,
            service=self.service,
            appointment_date=date.today() + timedelta(days=2),
            appointment_time='09:00'
        )
        Appointment.objects.create(
            patient=self.user,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='11:00'
        )
        appointments = Appointment.objects.all()
        self.assertEqual(appointments[0].appointment_date, date.today() + timedelta(days=2))


class DoctorModelTests(TestCase):
    """Тесты для модели врача"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='doctor',
            password='pass123',
            is_doctor=True
        )

    def test_create_doctor(self):
        doctor = Doctor.objects.create(
            user=self.user,
            specialty='Cardiologist',
            education='Medical University',
            experience=10,
            is_active=True
        )
        self.assertEqual(doctor.specialty, 'Cardiologist')
        self.assertEqual(doctor.experience, 10)
        self.assertTrue(doctor.is_active)
        self.assertEqual(str(doctor), 'Доктор  (Cardiologist)')


class AppointmentCreateTests(TestCase):
    """Тесты создания записей"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='patient',
            password='pass123',
            is_patient=True
        )
        self.category = ServiceCategory.objects.create(name='Diagnostics')
        self.service = Service.objects.create(
            name='MRI',
            category=self.category,
            price=5000,
            duration=60,
            description='MRI scan'
        )
        self.create_url = reverse('appointments:create')
        self.client.login(username='patient', password='pass123')

    def test_create_page_accessible(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/create.html')

    def test_create_appointment_success(self):
        tomorrow = date.today() + timedelta(days=1)
        response = self.client.post(self.create_url, {
            'service': self.service.id,
            'appointment_date': tomorrow.isoformat(),
            'appointment_time': '10:00',
            'notes': 'Test notes'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.status, 'pending')
        self.assertEqual(appointment.patient, self.user)

    def test_create_appointment_missing_fields(self):
        response = self.client.post(self.create_url, {
            'service': self.service.id,
            'appointment_date': '',
            'appointment_time': '10:00'
        })
        self.assertEqual(response.status_code, 200)  # Form error
        self.assertEqual(Appointment.objects.count(), 0)

    def test_create_with_service_from_query_param(self):
        response = self.client.get(f'{self.create_url}?service={self.service.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.name)

    def test_create_appointment_requires_login(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.create_url}')


class AppointmentListAndDetailTests(TestCase):
    """Тесты просмотра и деталей записей"""

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient',
            password='pass123',
            is_patient=True
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='pass123',
            is_patient=True
        )
        self.category = ServiceCategory.objects.create(name='Diagnostics')
        self.service = Service.objects.create(
            name='MRI',
            category=self.category,
            price=5000,
            duration=60,
            description='MRI scan'
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='pending'
        )
        self.client.login(username='patient', password='pass123')

    def test_list_view(self):
        response = self.client.get(reverse('appointments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.service.name)

    def test_cannot_access_others_appointment(self):
        self.client.logout()
        self.client.login(username='other', password='pass123')
        response = self.client.get(reverse('appointments:detail', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 404)  # Not found for other user

    def test_history_view(self):
        response = self.client.get(reverse('appointment_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/appointment_history.html')


class AppointmentCancelTests(TestCase):
    """Тесты отмены записей"""

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient',
            password='pass123',
            is_patient=True
        )
        self.category = ServiceCategory.objects.create(name='Diagnostics')
        self.service = Service.objects.create(
            name='MRI',
            category=self.category,
            price=5000,
            duration=60,
            description='MRI scan'
        )
        self.client.login(username='patient', password='pass123')

    def test_cancel_pending_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='pending'
        )
        response = self.client.post(reverse('appointments:cancel', args=[appointment.id]))
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, 'cancelled')

    def test_cancel_confirmed_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='confirmed'
        )
        response = self.client.post(reverse('appointments:cancel', args=[appointment.id]))
        self.assertEqual(response.status_code, 302)
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, 'cancelled')

    def test_cannot_cancel_completed_appointment(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='completed'
        )
        response = self.client.get(reverse('appointments:cancel', args=[appointment.id]))
        self.assertEqual(response.status_code, 404)

    def test_cancel_page_accessible_for_pending(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            service=self.service,
            appointment_date=date.today() + timedelta(days=1),
            appointment_time='10:00',
            status='pending'
        )
        response = self.client.get(reverse('appointments:cancel', args=[appointment.id]))
        self.assertEqual(response.status_code, 200)


class MainViewTests(TestCase):
    """Тесты главных страниц"""

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')

    def test_contacts_page(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/contacts.html')

    def test_contacts_form_submission(self):
        response = self.client.post(reverse('contacts'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+79991234567',
            'message': 'Hello, this is a test message'
        })
        self.assertEqual(response.status_code, 302)  # Redirect with success message