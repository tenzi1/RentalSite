from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"


def test_form_view(request):
    from .forms import CategoryForm

    form = CategoryForm()
    return render(request, "form.html", {"form": form})
