from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tictaktoe.views.hello', name='hello'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^hello', 'tictaktoe.views.hello', name='hello'),
    url(r'game$', 'tictaktoe.game.views.game', name='game'),
    

    url(r'^admin/', include(admin.site.urls)),
)
