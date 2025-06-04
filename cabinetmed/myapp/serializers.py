from rest_framework import serializers
from .models import Medecin, Patient, Consultation, DossierMedical, RendezVous


class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['id', 'cin', 'nom', 'prenom', 'telephone', 'email', 'accountType', 'specialite']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'cin', 'nom', 'prenom', 'telephone', 'email', 'accountType', 'date_naissance', 'genre']

class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'

class DossierMedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierMedical
        fields = '__all__'

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'