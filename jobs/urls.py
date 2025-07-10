from django.urls import path
from .views import JobCreateView, JobsRetrieveView

urlpatterns = [
    path('jobs', JobCreateView.as_view(), name='job-create'),
    path('jobs/<uuid:event_id>', JobsRetrieveView.as_view(), name='jobs-retrieve'),
] 