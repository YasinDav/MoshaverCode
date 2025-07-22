from account.urls import urlpatterns as account
from account.views import login_view, signup_view, logout_view, change_password_view
from consult.urls import urlpatterns as consult
from core import error_handlers
# from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from index.sitemaps import StaticViewSitemap
from index.urls import urlpatterns as index
from index.views import dashboard_view

dashboard_urlpatterns = [
    path('consult/', include(consult)),
    path('profile/', include(account)),
    path('', dashboard_view, name="dashboard")

]

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include(dashboard_urlpatterns)),
    path('', include(index)),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('changepw/', change_password_view, name="change_password"),
    path('summernote/', include('django_summernote.urls')),
    path(
        "sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt', include('robots.urls')),
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += debug_toolbar_urls()

handler403 = error_handlers.handler403
handler404 = error_handlers.handler404
handler405 = error_handlers.handler405
handler500 = error_handlers.handler500
