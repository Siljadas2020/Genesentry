
from django.contrib import admin
from django.urls import  path

from genesentryapp.views import *

urlpatterns = [
    path('', LoginView.as_view(),name='login'),
    path('admin_home', AdminHomeView.as_view(), name='admin_home'),
    path('add_doc', AddDoctorView.as_view(), name='add_doc'),
    path('govt_policy', GovtPolicyView.as_view(), name='govt_policy'),
    path('view_govt', ViewGovt.as_view(), name='view_govt'),
    path('view_govt_policy/<int:id>/', ViewGovtPolicy.as_view(), name='view_govt_policy'),
    path('manage_doctors', ManageDoctorsView.as_view(), name='manage_doctors'),
    path('update_doc/<int:id>/', UpdateDocView.as_view(), name='update_doc'),
    path('delete_doc/<int:id>/', DeleteDocView.as_view(), name='delete_doc'),
    path('verify_pharmacist', VerifyPharmacistView.as_view(), name='verify_pharmacist'),
    path('AcceptPharmacist/<int:id>/', AcceptPharmacist.as_view(), name='AcceptPharmacist'),
    path('RejectPharmacist/<int:id>/', RejectPharmacist.as_view(), name='RejectPharmacist'),
    path('view_appointments', ViewAppointmentsView.as_view(), name='view_appointments'),
    path('view_patients', ViewPatientsView.as_view(), name='view_patients'),
    path('view_review', ViewReviewView.as_view(), name='view_review'),
    path('appointments', AppointmentsView.as_view(), name='appointments'),
    path('medicalposts', MedicalPostsView.as_view(), name='medicalposts'),
    path('notification', NotificationView.as_view(), name='notification'),
    path('prescription', PrescriptionView.as_view(), name='prescription'),
    path('add', AddView.as_view(), name='add'),
    path('edit',EditView.as_view(), name='edit'),
    path('manage_medicine',ManageMedicineView.as_view(), name='manage_medicine'),
    path('Register',RegisterView.as_view(), name='Register'),
    path('Request',RequestView.as_view(), name='Request'),
]

