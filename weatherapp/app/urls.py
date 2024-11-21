from django.contrib import admin
from django.urls import path, include

from weather.views.errors import BadRequestErrorView, ForbiddenErrorView, NotFoundErrorView, ServerErrorView

handler400 = BadRequestErrorView()
handler403 = ForbiddenErrorView()
handler404 = NotFoundErrorView()
handler500 = ServerErrorView()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('users.urls', 'users'), namespace='accounts')),
    path('',  include(('weather.urls', 'weather'), namespace='weather'))
]
