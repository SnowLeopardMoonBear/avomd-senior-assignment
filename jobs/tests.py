import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from jobs.models import Job, JobStatus
import uuid

@pytest.mark.django_db
def test_job_create_and_retrieve():
    client = APIClient()
    # 1. Job create API
    input_text = "test input"
    create_url = reverse('job-create')
    response = client.post(create_url, {"input_text": input_text}, format='json')
    assert response.status_code == 200
    event_id = response.data['event_id']
    assert event_id is not None

    # 2. Check if the job is created in the database
    job = Job.objects.get(event_id=event_id)
    assert job.input_text == input_text
    assert job.status in [JobStatus.PENDING, JobStatus.PROCESSING]

    # 3. Job retrieve API (checklist is not yet available)
    retrieve_url = reverse('jobs-retrieve', kwargs={'event_id': event_id})
    response = client.get(retrieve_url)
    assert response.status_code == 200
    assert response.data['status'] in [JobStatus.PENDING, JobStatus.PROCESSING]
    assert response.data['result'] is None

@pytest.mark.django_db
def test_job_retrieve_404():
    client = APIClient()
    fake_event_id = uuid.uuid4()
    retrieve_url = reverse('jobs-retrieve', kwargs={'event_id': fake_event_id})
    response = client.get(retrieve_url)
    assert response.status_code == 404
    assert response.data['detail'] == 'Job not found.'
