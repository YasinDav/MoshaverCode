from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from index.urls import urlpatterns as index
from account.urls import urlpatterns as account
from account.views import login_view, signup_view, logout_view
from consult.urls import urlpatterns as consult


dashboard_urlpatterns = [
    path('consult/', include(consult)),
    path('profile/', include(account)),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(dashboard_urlpatterns)),
    path('', include(index)),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
