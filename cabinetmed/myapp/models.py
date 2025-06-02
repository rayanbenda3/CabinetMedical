from django.db import models


class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    cin = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    accountType = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom} {self.prenom} (CIN: {self.cin})"


class Patient(Utilisateur):
    date_naissance = models.DateField()
    genre = models.CharField(max_length=10)

    def __str__(self):
        return f"Patient: {self.nom} {self.prenom} (CIN: {self.cin})"


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
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
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
