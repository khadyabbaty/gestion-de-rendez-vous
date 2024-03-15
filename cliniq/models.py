
from django.urls import reverse
from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager



class CliniqUser (AbstractUser):
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField('Is Admin',default=False)
    is_specialiste= models.BooleanField('Is Specialiste',default=False)
    is_gerent = models.BooleanField('Is Gerent',default=False)
    nom = models.CharField(max_length=200)
    prénom = models.CharField(max_length=200)
        
    def get_absolute_url(self):
        return reverse("dashbord")
    
class Gerent(models.Model):
    user = models.ForeignKey(CliniqUser, on_delete=models.CASCADE)
    

SPECIALITE_CHOICES =[
        ("Pediatrie","Pediatrie"),
        ("Dentiste","Dentiste"),
        ("Dermatologist","Dermatologist"),
    ]
class Specialiste(models.Model):
    user = models.ForeignKey(CliniqUser, on_delete=models.CASCADE)
    spécialité = models.CharField(max_length=200,choices=SPECIALITE_CHOICES)
    nbr_max_rdv = models.IntegerField(default=False)
    
    
    def __str__(self):
        return self.user.nom +" "+self.user.prénom+" (" + self.spécialité+")"

    
class Patient(models.Model):
    nom = models.CharField(max_length=200)
    prénom = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
    Tél = models.CharField(max_length=8)

    def get_absolute_url(self):
        return reverse("RDV", kwargs={"pk": self.pk})

    def __str__(self):
        return self.nom



class RDV (models.Model):
    patient = models.ForeignKey(Patient, null=False, blank=False,
                                on_delete=models.CASCADE, related_name='patient_rdv')
    spécialiste = models.ForeignKey(Specialiste, on_delete=models.PROTECT ,related_name='sp_rdv')
    date = models.DateField()
    temp = models.TimeField()

    def get_success_url(self):
        return reverse_lazy('RDV', kwargs={'pk': self.object.patient_id})
