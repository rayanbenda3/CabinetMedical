from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedecinViewSet, PatientViewSet

router = DefaultRouter()
router.register(r'medecins', MedecinViewSet)
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
