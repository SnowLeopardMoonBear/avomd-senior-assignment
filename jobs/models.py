from django.db import models
import uuid

class JobStatus(models.TextChoices):
    PENDING = 'pending', 'Pending' # The job is created but not yet processed.
    PROCESSING = 'processing', 'Processing' # The job is being processed.
    COMPLETED = 'completed', 'Completed' # The job is completed.
    FAILED = 'failed', 'Failed' # The job failed.

class Job(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="The unique identifier for the job.") 
    status = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.PENDING, help_text="The status of the job.")
    summary = models.TextField(blank=True, help_text="The summary returned by the first GPT Chain.")
    checklist = models.TextField(blank=True, help_text="The checklist returned by the second GPT Chain.")
    input_text = models.TextField(blank=True, help_text="The input text of the job.")
    job_created_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the job is created.")
    job_finished_at = models.DateTimeField(null=True, blank=True, help_text="The timestamp when the job is finished.")

    class Meta:
        # For further search and filtering, added some indices.
        indexes = [
            models.Index(fields=['job_created_at']),
            models.Index(fields=['job_finished_at']),
            models.Index(fields=['status', 'job_created_at']),
        ]
        ordering = ['-job_created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"Job {self.event_id} [{self.status}]"
