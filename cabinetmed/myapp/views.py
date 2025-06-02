from rest_framework import viewsets
from .serializers import MedecinSerializer, PatientSerializer
from .models import Medecin
from .models import Patient

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
# Create your views here.
