"""prototype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from typing import List
from django.contrib import admin
from django.urls import path
from djavue.views import VuetifyTemplate


class Index(VuetifyTemplate):
    def get_context(self, request):
        return {"app": "Djavue"}

    def get_template_name(self, request) -> str:
        if request.user.is_anonymous:
            return "Login.vue"

        return "Login.vue"

    class Meta:
        page_title = "Homepage"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
]
