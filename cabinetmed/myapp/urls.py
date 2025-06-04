from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedecinViewSet, PatientViewSet, ConsultationViewSet, DossierMedicalViewSet, RendezVousViewSet

router = DefaultRouter()
router.register(r'medecins', MedecinViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'dossiers', DossierMedicalViewSet)
router.register(r'rendezvous', RendezVousViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
