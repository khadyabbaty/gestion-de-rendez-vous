from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from.views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),

    path('logout/', views.logout, name='logout'),
    
    path('dashbord/', UserList,  name='dashbord'),
    
    
    path('dashbord/add_specialiste/', SpecialisteCreateView.as_view(), name='add_specialiste'),
    path('dashbord/specialiste/<int:pk>/update_specialiste/', SpecialisteUpdateView.as_view(), name='update_specialiste'),
    path('dashbord/specialiste/<int:pk>/delete_specialiste/', SpecialisteDeleteView.as_view(), name='delete_specialiste'),
    
    
    path('dashbord/add_gerent/', GerentCreateView.as_view(), name='add_gerent'),
    path('dashbord/gerent/<int:pk>/update_gerent/', GerentUpdateView.as_view(), name='update_gerent'),
    path('dashbord/gerent/<int:pk>/delete_gerent/',GerentDeleteView.as_view(), name='delete_gerent'),
    
    
    path('specialiste/<int:pk>', SpecialistePatient, name='specialiste'),

    path('patients/', login_required(PatientListView.as_view(),
         login_url='login'), name='patients'),

    path('patients/add', login_required(PatientCreateView.as_view(),
         login_url='login'), name='add_patient'),

    path('patients/<int:pk>/update', login_required(PatientUpdateView.as_view(),
         login_url='login'), name='modifier_patient'),

    path('patients/<int:pk>/delete', login_required(PatientDeleteView.as_view(),
         login_url='login'), name='suprimer_patient'),

    path('rdv/<str:pk>', login_required(PatientDetailView.as_view(),
         login_url='login'), name='RDV'),

    path('rdv/<str:pk>/ajouter', login_required(RDVCreateView.as_view(),
         login_url='login'), name='add_rdv'),

    path('rdv/<str:pk>/delete', login_required(RDVDeleteView.as_view(),
         login_url='login'), name='delete_rdv'),

    path('rdv/<str:pk>/update', login_required(RDVUpdateView.as_view(),
         login_url='login'), name='update_rdv'),

]
