"""
URL configuration for drf_book_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book import views as book_views
from auth_app import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from .settings import base_settings
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r"author", book_views.AuthorViewSet)
router.register(r"book", book_views.BookViewSet)
router.register(r"language", book_views.LanguageViewSet)
router.register(r"user", auth_views.UserViewSet, basename="user")
router.register(r"review", book_views.ReviewViewSet)
router.register(r"address", auth_views.AddressViewSet, basename="address")
router.register(r"cart", auth_views.CartViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)