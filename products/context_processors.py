from .forms import ProductSearchForm
from products.models import Category


def search_form(request):
    return {"search_form": ProductSearchForm()}


def categories(request):
    return {
        "categories": {
            category.slug: category.name for category in Category.objects.all()
        }
    }
