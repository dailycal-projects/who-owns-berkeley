from django.conf.urls import url
from django.contrib import admin
from parcels.views import *

urlpatterns = [
	url(r'^$', Main.as_view()),
    url(r'^api/parcels.json$', ParcelsJson.as_view(), name='parcels-json'),
    url(r'^admin/', admin.site.urls),
]
