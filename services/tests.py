from django.test import TestCase
from django.urls import reverse
from services.models import Service, ServiceCategory


class ServiceModelTests(TestCase):
    """Тесты для модели услуг"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            icon='bi-stethoscope',
            description='Медицинская диагностика'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Диагностика')
        self.assertEqual(str(self.category), 'Диагностика')

    def test_service_creation(self):
        service = Service.objects.create(
            name='МРТ',
            category=self.category,
            price=5000,
            duration=60,
            description='Магнитно-резонансная томография',
            is_active=True
        )
        self.assertEqual(service.name, 'МРТ')
        self.assertEqual(service.price, 5000)
        self.assertEqual(str(service), 'МРТ - 5000 руб.')
        self.assertTrue(service.is_active)


class ServiceViewTests(TestCase):
    """Тесты для представлений услуг"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            icon='bi-stethoscope'
        )
        self.service = Service.objects.create(
            name='МРТ',
            category=self.category,
            price=5000,
            duration=60,
            description='МРТ исследование',
            is_active=True,
            slug='mrt'
        )

    def test_service_list_view(self):
        response = self.client.get(reverse('services:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/list.html')
        self.assertContains(response, 'Диагностика')
        self.assertContains(response, 'МРТ')

    def test_service_detail_404_for_inactive(self):
        self.service.is_active = False
        self.service.save()
        response = self.client.get(reverse('services:detail', args=['mrt']))
        self.assertEqual(response.status_code, 404)

    def test_service_detail_404_for_wrong_slug(self):
        response = self.client.get(reverse('services:detail', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)
