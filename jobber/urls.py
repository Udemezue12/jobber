"""
URL configuration for jobber project.

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
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('job', include('jobber.urls')),
    path('', include('applicants.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'applicants.views.bad_request'
handler403 = 'applicants.views.forbidden'
handler404 = 'applicants.views.page_not_found'
handler500 = 'applicants.views.internal_server_error'
