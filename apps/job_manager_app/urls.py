from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^regprocess$', views.user),
    url(r'^jobs/new$', views.registration),
    url(r'^loginprocess$', views.login_process),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^jobprocess$', views.job_process),  
    url(r'^dashboard$', views.jobs),    
    url(r'^job/(?P<jobid>\w+)/delete$', views.remove_job),
    url(r'^job/update/(?P<jobid>\w+)$', views.update),
    url(r'^jobs/edit/(?P<jobid>\w+)$', views.edit_job),
    url(r'^add/(?P<jobid>\w+)$', views.add),
    url(r'^giveup/(?P<jobid>\w+)$', views.giveup),
    url(r'^jobs/(?P<jobid>\w+)$', views.details)
]