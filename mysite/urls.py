"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from mysite.coresettings.appconf import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
]

#when the debug is True
if settings.DEBUG:
	
	urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	
#Installing Administration App
if Main.run:
	urlpatterns.append(path('',include('Applications.Main.urls',namespace='Main')))
else:
	pass
     
#Installing Administration App
if Administration.run:
	urlpatterns.append(path('',include('Applications.Administration.urls',namespace='Admin')))
else:
	pass
	
#Installing Administration App
if Examination.run:
    urlpatterns.append(path('Exams/',include('Applications.Examination.urls',namespace='Exams')))
else:
	pass
	
#Installing Administration App	
if Transactions.run:
    urlpatterns.append(path('Transactions/',include('Applications.Transactions.urls',namespace='Transactions')))
else:
	pass	

#Installing Administration App
if Education.run:
    urlpatterns.append(path('',include('Applications.Education.urls',namespace='Education')))
else:
	pass	


	
#Installing Administration App	
if Management.run:
    urlpatterns.append(path('Management/',include('Applications.Management.urls',namespace='Management')))
else:
	pass

#Installing Administration App	
if DashBoard.run:
    urlpatterns.append(path('DashBoard/',include('Applications.DashBoard.urls',namespace='DashBoard')))
else:
	pass



