from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Service, ServiceCategory


def service_list(request):
    """Список всех услуг"""
    try:
        categories = ServiceCategory.objects.prefetch_related('services').all()
        context = {
            'title': 'Наши услуги',
            'categories': categories,
        }
        return render(request, 'services/list.html', context)

    except ServiceCategory.DoesNotExist:
        # Категорий нет в базе
        return render(request, 'services/list.html', {'categories': []})

    except Exception as e:
        # Логируем неожиданную ошибку (но конкретные исключения выше уже обработаны)
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in service_list: {str(e)}")

        return HttpResponse("""
        <h1>Ошибка загрузки услуг</h1>
        <p>Попробуйте позже или свяжитесь с администратором</p>
        <a href="/">На главную</a>
        """, status=500)


def service_detail(request, slug):
    """Детальная информация об услуге"""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    similar_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:5]

    context = {
        'title': service.name,
        'service': service,
        'similar_services': similar_services,
        'today': timezone.now().date(),
    }
    return render(request, 'services/detail.html', context)