from rest_framework import serializers
from .models import Medecin, Patient

class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['id', 'cin', 'nom', 'prenom', 'telephone', 'email', 'accountType', 'specialite']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'cin', 'nom', 'prenom', 'telephone', 'email', 'accountType', 'date_naissance', 'genre']
