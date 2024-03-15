from django.shortcuts import redirect, render,get_object_or_404
from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import(
    CreateView, ListView, TemplateView, DetailView, FormView, UpdateView, DeleteView, View,)
from django.urls import reverse_lazy
from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class PatientListView(ListView):
    model = Patient
    template_name = 'cliniq/patient.html'
    context_object_name = 'patient'


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'cliniq/add_patient.html'

    def form_valid(self, form):

        return super().form_valid(form)


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'cliniq/RDV.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    pk_url_kwarg = 'pk'
    template_name = 'cliniq/update_patient.html'
    success_url = reverse_lazy('patients')


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('patients')


class RDVCreateView(CreateView):
    model = RDV
    form_class = RDV_form
    template_name = 'cliniq/add_rdv.html'

    def get_initial(self):
        initial = super(RDVCreateView, self).get_initial()
        initial['patient'] = Patient.objects.get(pk=self.kwargs["pk"])
        return initial

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('RDV', kwargs={'pk': self.object.patient_id})


class RDVDeleteView(DeleteView):
    model = RDV

    def get_success_url(self):
        return reverse_lazy('RDV', kwargs={'pk': self.object.patient_id})


class RDVUpdateView(UpdateView):
    model = RDV
    form_class = RDV_form
    pk_url_kwarg = 'pk'
    template_name = 'cliniq/update_rdv.html'

    def get_success_url(self):
        return reverse_lazy('RDV', kwargs={'pk': self.object.patient_id})


class GerentCreateView(CreateView):
    model = CliniqUser
    form_class = GerentCreationForm
    template_name = 'cliniq/add_gerent.html'


def UserList(request):
    sps = Specialiste.objects.all()
    grs = Gerent.objects.all()
    context = {'sps': sps, 'grs': grs}
    return render(request, 'cliniq/admin.html', context)


class GerentUpdateView(UpdateView):
    model = Gerent
    form_class = GerentCreationForm
    template_name = 'cliniq/update_gerent.html'
    context_object_name = 'users'


class GerentDeleteView(DeleteView):
    Model = Gerent


class SpecialisteCreateView(CreateView):
    model = CliniqUser
    form_class = SpecialisteCreationForm
    template_name = 'cliniq/add_specialiste.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashbord')
    



class SpecialisteUpdateView(UpdateView):
    model = CliniqUser
    form_class = SpecialisteUpdateForm
    template_name = 'cliniq/update_specialiste.html'
    context_object_name = 'users'


class SpecialisteDeleteView(DeleteView):
    Model = Specialiste


class LoginView(View):
    template_name = 'cliniq/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                if user.is_gerent:
                    return redirect('patients')
                elif user.is_specialiste:
                    pk=user.id
                    return redirect('specialiste',pk)
                else:
                    return redirect('dashbord')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
        return render(request, self.template_name, {'form': form},)


def logout(request):
    user_logout(request)
    return redirect('login')


def SpecialistePatient(request, pk):
    rdv=RDV.objects.filter(spécialiste_id=pk)
    return render(request,'cliniq/specialiste.html', {'rdv': rdv})
# class SpecialistePatient(ListView):
#     model = RDV
#     template_name = 'cliniq/specialiste.html'
#     context_object_name = 'rdv'
    
# return RDV.objects.filter(spécialiste_id=request.POST.get('spécialiste_i'))