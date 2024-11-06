from django.db import models
from django_lifecycle import LifecycleModelMixin
from core.settings import AUTH_USER_MODEL

class BaseContent(LifecycleModelMixin,models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True,max_length=20,choices=(
        (True,'Active'),
        (False,'inactive')
    ))
    
    class Meta:
        abstract = True