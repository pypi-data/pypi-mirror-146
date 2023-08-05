from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from simpel_payments.models import Payment


@receiver(post_save, sender=Payment)
def after_save_receipt(sender, instance, **kwargs):
    if instance.reference is not None:
        instance.reference.save()

    if instance.qrcodes.first() is None:
        instance.qrcodes.create(name="public_url", qr_data=instance.admin_url)


@receiver(post_delete, sender=Payment)
def after_delete_receipt(sender, instance, **kwargs):
    if instance.reference is not None:
        instance.reference.save()
