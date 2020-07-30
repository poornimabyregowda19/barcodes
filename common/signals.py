from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def full_clean_hook(sender, instance, *args, **kwargs):
    if sender.__name__ != 'Session':
        instance.full_clean()
