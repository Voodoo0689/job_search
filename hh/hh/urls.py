"""hh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
import mainapp.views as mainapp
import authapp.views as authapp
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from mainapp.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="HH",
        default_version='1.0',
        description="Documentation to HH project",
        contact=openapi.Contact(email="admin@admin.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register('Users', UserModelViewSet)
router.register('City', CityModelViewSet)
router.register('Roles', RolesModelViewSet)

router.register('UserProfile', UserProfileModelViewSet)
router.register('CompanyProfile', CompanyProfileModelViewSet)
router.register('UserEdu', UserEduModelViewSet)

router.register('UserJobHistory', UserJobHistoryModelViewSet)
router.register('Articles', ArticlesModelViewSet)
router.register('Vacancy', VacancyModelViewSet)
router.register('Resumes', ResumesModelViewSet)

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('admin/', admin.site.urls),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('company-profile/', include('companyapp.urls', namespace='companies')),
    path('user_profile/', include('userapp.urls', namespace='users')),
    re_path(r'^partners/', include('mainapp.urls', namespace='partners')),
    re_path(r'^articles/', include('mainapp.urls', namespace='articles')),
    re_path(r'^vacancies/', include('mainapp.urls', namespace='vacancies')),
    path('about/', mainapp.about, name='about'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui.html'),
    path('redoc/', schema_view.with_ui('redoc', )),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
