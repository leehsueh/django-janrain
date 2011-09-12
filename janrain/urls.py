from django.conf.urls.defaults import *

urlpatterns = patterns('myproject.janrain.views',
    url(r'^login/$',
        'login',
        name='janrain-login'
    ),
    url(r'^logout/$',
        'logout',
        name='janrain-logout'
    ),
)