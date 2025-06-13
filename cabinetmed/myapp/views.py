from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MedecinSerializer, PatientSerializer, ConsultationSerializer, DossierMedicalSerializer, \
    RendezVousSerializer
from .models import Medecin, Consultation, DossierMedical, RendezVous, Utilisateur
from .models import Patient

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
# Create your views here.

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer

class DossierMedicalViewSet(viewsets.ModelViewSet):
    queryset = DossierMedical.objects.all()
    serializer_class = DossierMedicalSerializer

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer

class SignupView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        nom = data.get('nom')
        prenom = data.get('prenom')
        cin = data.get('cin')
        accountType = data.get('accountType')
        telephone = data.get('telephone')

        if Utilisateur.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = Utilisateur.objects.create_user(
            cin=cin,
            email=email,
            password=password,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            accountType=accountType,
        )

        # Synchronisation Neo4j automatique
        from services.neo4jsvc import upsert_patient, upsert_medecin
        if accountType == "Patient":
            upsert_patient(user)
        elif accountType == "Medecin":
            upsert_medecin(user)

        return Response({"message": "Compte créé"}, status=status.HTTP_201_CREATED)


class SigninView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'email': user.email,
                    'type': user.accountType
                }
            })
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
