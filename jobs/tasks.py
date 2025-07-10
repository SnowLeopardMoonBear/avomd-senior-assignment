from celery import shared_task
from .models import Job, JobStatus
from django.utils import timezone
import openai
import os
import logging

def call_openai_sync(prompt):
    """
    Calls the OpenAI API synchronously with the given prompt and returns the response content.
    """
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@shared_task
def process_job_task(event_id, input_text):
    """
    Celery task to process a Job: summarizes the input_text and generates a checklist using OpenAI API.
    Updates the Job model with the results and status.
    If summarize step fails, status is set to FAILED and no summary is saved.
    If checklist step fails, summary is saved, checklist is empty, and status is set to FAILED.
    """
    job = Job.objects.get(event_id=event_id)
    try:
        summary = call_openai_sync(f"Summarize: {input_text}")
        job.summary = summary
        job.save()
        try:
            checklist = call_openai_sync(f"Generate a checklist for: {summary}")
            job.checklist = checklist
            job.status = JobStatus.COMPLETED
            job.job_finished_at = timezone.now()
            job.save()
        except Exception as e:
            logging.exception(f"Celery task checklist step failed for event_id={event_id}: {e}")
            job.status = JobStatus.FAILED
            job.job_finished_at = timezone.now()
            job.save()
    except Exception as e:
        logging.exception(f"Celery task summarize step failed for event_id={event_id}: {e}")
        job.status = JobStatus.FAILED
        job.job_finished_at = timezone.now()
        job.save() 