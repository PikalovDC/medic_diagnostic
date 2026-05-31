from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Service, ServiceCategory


def service_list(request):
    """Список всех услуг"""
    try:
        categories = ServiceCategory.objects.prefetch_related('services').all()

        print(f"[DEBUG] Категорий: {categories.count()}")

        context = {
            'title': 'Наши услуги',
            'categories': categories,
        }

        # ИСПРАВЛЕНО: используем list.html вместо list_simple.html
        return render(request, 'services/list.html', context)

    except Exception as e:
        print(f"[ERROR] service_list: {str(e)}")
        import traceback
        traceback.print_exc()

        return HttpResponse(f"""
        <h1>Ошибка загрузки услуг</h1>
        <p>Произошла ошибка: {str(e)}</p>
        <a href="/">На главную</a>
        """)


def service_detail(request, slug):
    """Детальная информация об услуге"""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # Получаем похожие услуги из той же категории
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