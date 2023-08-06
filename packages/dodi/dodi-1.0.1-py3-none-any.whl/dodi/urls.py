from django.urls import path
from ._views import ImageResponder

urlpatterns = [
    path('<transform>/<path:source>', ImageResponder.handle, name='dodi_image')
]