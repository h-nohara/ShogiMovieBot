from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^account/", include("accounts.urls")),
    url(r"^board/", include("board.urls")),
]
