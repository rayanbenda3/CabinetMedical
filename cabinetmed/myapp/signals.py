from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Patient, Medecin, Consultation
from .services.neo4jsvc import (
    upsert_patient, delete_patient,
    upsert_medecin, delete_medecin,
    create_consultation_relation, delete_consultation_relation
)


@receiver(post_save, sender=Patient)
def sync_patient_to_neo4j(sender, instance, **kwargs):
    upsert_patient(instance)

@receiver(post_delete, sender=Patient)
def remove_patient_from_neo4j(sender, instance, **kwargs):
    delete_patient(instance.id)

@receiver(post_save, sender=Medecin)
def sync_medecin_to_neo4j(sender, instance, **kwargs):
    upsert_medecin(instance)

@receiver(post_delete, sender=Medecin)
def remove_medecin_from_neo4j(sender, instance, **kwargs):
    delete_medecin(instance.id)

@receiver(post_save, sender=Consultation)
def sync_consultation_to_neo4j(sender, instance, **kwargs):
    create_consultation_relation(instance)

@receiver(post_delete, sender=Consultation)
def remove_consultation_from_neo4j(sender, instance, **kwargs):
    delete_consultation_relation(instance)