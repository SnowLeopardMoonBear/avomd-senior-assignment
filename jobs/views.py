from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from .serializers import JobCreateRequestSerializer, JobCreateResponseSerializer, JobsRetrieveResponseSerializer
from .models import Job, JobStatus
from .tasks import process_job_task
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema


class JobCreateView(APIView):
    """
    API View to create a new Job and register a Celery async task. Returns the event_id of the created Job.
    """
    @swagger_auto_schema(
        request_body=JobCreateRequestSerializer,
        responses={201: JobCreateResponseSerializer}
    )
    def post(self, request):
        """
        Create a Job with the given input_text, register a Celery task, and return the event_id.
        """
        input_text = request.data.get('input_text', '')
        job = Job.objects.create(input_text=input_text)
        # To prevent race condition, we use transaction.on_commit to enqueue the task after the job is created.
        def enqueue_task():
            process_job_task.delay(job.event_id, job.input_text)
        transaction.on_commit(enqueue_task)
        job.status = JobStatus.PROCESSING
        job.save()
        return Response({'event_id': str(job.event_id)})

class JobsRetrieveView(APIView):
    """
    API View to retrieve a Job by event_id and return its status and checklist.
    """
    @swagger_auto_schema(
        responses={200: JobsRetrieveResponseSerializer},
        operation_description="Retrieve the Job with the given event_id and return its status and checklist. If the Job does not exist, return 404."
    )
    def get(self, request, event_id):
        """
        Retrieve the Job with the given event_id and return its status and checklist.
        If the Job does not exist, return 404.
        """
        try:
            job = Job.objects.get(event_id=event_id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=drf_status.HTTP_404_NOT_FOUND)
        return Response({
            "status": job.status,
            "result": job.checklist if job.checklist else None
        })
