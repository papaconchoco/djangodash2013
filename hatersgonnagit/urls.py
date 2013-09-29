from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', 'hatersgonnagit.views.home_view',
        name='home_view'),

    url(r'^(?P<repo_user>[^/]+)/(?P<repo_name>[^/]+)/comments/$',
        'hatersgonnagit.views.comments_view',
        name='comments_view'),
    url(r'^(?P<repo_user>[^/]+)/(?P<repo_name>[^/]+)/commits/$',
        'hatersgonnagit.views.commits_view',
        name='commits_view'),
    url(r'^(?P<repo_user>[^/]+)/(?P<repo_name>[^/]+)/issues/$',
        'hatersgonnagit.views.issues_view',
        name='issues_view'),

    url(r'^(?P<repo_user>[^/]+)/(?P<repo_name>[^/]+)/$',
        'hatersgonnagit.views.repo_view',
        name='repo_view'),

    # Examples:
    # url(r'^$', 'hatersgonnagit.views.home', name='home'),
    # url(r'^hatersgonnagit/', include('hatersgonnagit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
