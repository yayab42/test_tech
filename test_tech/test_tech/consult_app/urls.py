from django.urls import path
from .views import patient_list, patient_create, patient_update, patient_delete, login_user, logout_user, patient_profile, consultation_create, consultation_delete, consultation_update

urlpatterns = [
    path('', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('patients/', patient_list, name='patient-list'),
    path('patient/<str:username>/', patient_profile, name='patient-profile'),
    path('patients/create/', patient_create, name='patient-create'),
    path('patients/<str:username>/update/', patient_update, name='patient-update'),
    path('patients/<str:username>/delete/', patient_delete, name='patient-delete'),
    path('patients/<str:username>/consultation/create/', consultation_create, name='consultation-create'),
    path('consultations/<int:consultation_id>/delete/', consultation_delete, name='consultation-delete'),
    path('patients/<str:username>/consultations/update/<int:consultation_id>/', consultation_update, name='consultation-update'),

]
