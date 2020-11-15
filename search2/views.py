from django.shortcuts import render
from django.db.models import Q
from core.models import Item
from django.views.generic import TemplateView, ListView

class Csearchpage(TemplateView):
    template_name = 'csearch2.html'

class Csearch(ListView):
    model = Item
    template_name = 'csearch2.html'
    

    def get_queryset(self): # new
            query = self.request.GET.get('q')
            object_list = Item.objects.filter(
                 Q(title__icontains=query)
            )
            return object_list
# Create your views here.
