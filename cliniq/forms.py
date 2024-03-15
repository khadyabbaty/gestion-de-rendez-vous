
from django import forms
from django.db import transaction
from django.forms import ModelForm
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm


class SpecialisteCreationForm(UserCreationForm):
    nom = forms.CharField(required=True)
    prénom = forms.CharField(required=True)
    spécialité = forms.ChoiceField(choices=SPECIALITE_CHOICES)
    nbr_max_rdv = forms.IntegerField(required=True)
    

    class Meta(UserCreationForm.Meta):
        model = CliniqUser
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_specialiste = True
        user.nom = self.cleaned_data.get('nom')
        user.prénom = self.cleaned_data.get('prénom')
        user.save()
        specialiste = Specialiste.objects.create(user=user)
        specialiste.spécialité=self.cleaned_data.get('spécialité')
        specialiste.nbr_max_rdv=self.cleaned_data.get('nbr_max_rdv')
        specialiste.save()
        return user
    
    
    
class SpecialisteUpdateForm(UserChangeForm):
    
    class Meta(UserChangeForm.Meta):
        model = CliniqUser
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_specialiste = True
        user.nom = self.cleaned_data.get('nom')
        user.prénom = self.cleaned_data.get('prénom')
        user.save()
        specialiste = Specialiste.objects.update(user=user)
        specialiste.save()
        return user
        



class GerentCreationForm(UserCreationForm):
    nom = forms.CharField(required=True)
    prénom = forms.CharField(required=True)
    class Meta(UserCreationForm.Meta):
        model = CliniqUser
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_gerent = True
        user.nom = self.cleaned_data.get('nom')
        user.prénom = self.cleaned_data.get('prénom')
        user.save()
        gerent = Gerent.objects.create(user=user)
        gerent.save()
        return user




    # def __init__(self, *args, **kwargs):
    #       super().__init__(*args, **kwargs)
    #       for field in self.fields.values():
    #           if field:
    #               field.widget.attrs.update({'class': 'form-control'})


#   def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#     MY NAME IS CHEIKH BEOUMAR SOFTWER INGENIER TRANERSHIP IN SMART MS SA     if field.widget:
#              field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    class Meta:
        model = CliniqUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PatientForm (ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RDV_form(ModelForm):
    class Meta:
        model = RDV
        fields = '__all__'

        patient = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'temp': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
