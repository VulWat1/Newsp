from django.shortcuts import render
from .models import Articles
from django.views.generic import DetailView

# Create your views here.
def news(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/index.html', {'news': news})

class NewsDet(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'