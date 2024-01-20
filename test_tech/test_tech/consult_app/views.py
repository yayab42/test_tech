from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Patient


class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Patient
    template_name = 'patient_list.html'
    context_object_name = 'patients'

    def test_func(self):
        return self.request.user.is_doctor


class PatientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Patient
    template_name = 'patient_form.html'
    fields = ['patient_id', 'first_name', 'last_name', 'email', 'address']

    def test_func(self):
        return self.request.user.is_doctor


class PatientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    template_name = 'patient_form.html'
    fields = ['patient_id', 'first_name', 'last_name', 'email', 'address']

    def test_func(self):
        return self.request.user.is_doctor


class PatientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Patient
    template_name = 'patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

    def test_func(self):
        return self.request.user.is_doctor
