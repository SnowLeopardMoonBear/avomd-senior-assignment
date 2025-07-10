from rest_framework import serializers
from .models import Job, JobStatus
import uuid

class JobCreateRequestSerializer(serializers.Serializer):
    input_text = serializers.CharField()

class JobCreateResponseSerializer(serializers.Serializer):
    event_id = serializers.UUIDField()

class JobsRetrieveResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    result = serializers.CharField(allow_null=True, required=False) 