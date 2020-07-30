from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string
from .constants import UID_LENGTH

class UIDMixin(object):
    def get_uid(self):
        if not self.uid:
            self.uid = get_random_string(length=UID_LENGTH)
    def clean(self):
        self.get_uid()

class BaseModel(models.Model,UIDMixin):
    uid = models.CharField(max_length=32, null=False, blank=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

