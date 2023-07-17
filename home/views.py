from django.shortcuts import render
from django import views


class HomeView(views.View):
    template_name = 'home/landing_page.html'

    def get(self, request):
        return render(request, self.template_name)