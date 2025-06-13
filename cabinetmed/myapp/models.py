from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.db import models


class UtilisateurManager(BaseUserManager):
    def create_user(self, cin, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(cin=cin, email=email, **extra_fields)
        user.set_password(password)  # crypte le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, cin, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('accountType', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(cin, email, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('medecin', 'Médecin'),
        ('admin', 'Administrateur'),
    )

    cin = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    accountType = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cin', 'nom', 'prenom']

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"


class Patient(Utilisateur):
    date_naissance = models.DateField()
    genre = models.CharField(max_length=10)

    def __str__(self):
        return f"Patient: {self.nom} {self.prenom} ({self.email})"

class Medecin(Utilisateur):
    specialite = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.nom} {self.prenom} - {self.specialite}"


class Consultation(models.Model):
    id = models.AutoField(primary_key=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    motif = models.TextField()
    date = models.DateField()
    prescription = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    def __str__(self):
        return f"Consultation on {self.date} - Patient: {self.patient.nom} {self.patient.prenom}, Dr: {self.medecin.nom} {self.medecin.prenom}"


class DossierMedical(models.Model):
    id = models.AutoField(primary_key=True)
    date_naissance = models.DateField()
    contact = models.CharField(max_length=20)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dossier médical de {self.nom} {self.prenom}"


class RendezVous(models.Model):
    id = models.AutoField(primary_key=True)
    date_rdv = models.DateTimeField()
    description = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)

    def __str__(self):
        return f"RDV on {self.date_rdv.strftime('%Y-%m-%d %H:%M')} - Patient: {self.patient.nom} {self.patient.prenom}, Dr: {self.medecin.nom} {self.medecin.prenom}"
