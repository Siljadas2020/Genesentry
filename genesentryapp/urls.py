
from django.contrib import admin
from django.urls import  path

from genesentryapp.views import *

urlpatterns = [
    path('', LoginView.as_view(),name='login'),
    path('logout', LogoutView.as_view(),name='logout'),
    path('admin_home', AdminHomeView.as_view(), name='admin_home'),
    path('add_doc', AddDoctorView.as_view(), name='add_doc'),
    path('govt_policy', GovtPolicyView.as_view(), name='govt_policy'),
    path('view_govt', ViewGovt.as_view(), name='view_govt'),
    path('view_govt_policy/<int:id>/', ViewGovtPolicy.as_view(), name='view_govt_policy'),
    path('update_govt/<int:id>/', UpdateGovt.as_view(), name='update_govt'),
    path('delete_govt/<int:id>/', DeleteGovt.as_view(), name='delete_govt'),
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
    # path('notification', NotificationView.as_view(), name='notification'),
    path('prescription', PrescriptionView.as_view(), name='prescription'),
    path('add', AddView.as_view(), name='add'),
    path('edit',EditView.as_view(), name='edit'),
    path('manage_medicine',ManageMedicineView.as_view(), name='manage_medicine'),
    path('Request',RequestView.as_view(), name='Request'),

    path('doctor_home', DoctorHomeView.as_view(), name='doctor_home'),
    path('manage_prescription', ManagePrescriptionView.as_view(), name='manage_prescription'),
    path('update_prescription/<int:id>/', UpdatePrescription.as_view(), name='update_prescription'),
    path('delete_prescription/<int:id>/', DeletePrescription.as_view(), name='delete_prescription'),
    path('new_prescription', NewPrescriptionView.as_view(), name='new_prescription'),
    path('accept_prescription/<int:id>/', AcceptPrescription.as_view(), name='accept_prescription'),
    path('reject_prescription/<int:id>/', RejectPrescription.as_view(), name='reject_prescription'),
    # path('order', OrderView.as_view(), name='order'),
    path('view_order', ViewOrder.as_view(), name='view_order'),
    path('delete_order/<int:id>/', DeleteOrder.as_view(), name='delete_order'),
    path('status', StatusView.as_view(), name='status'),
    path('add_post', AddPostView.as_view(), name='add_post'),
    path("view_rating", ViewRatingView.as_view(), name="view_rating"),
    path("send_notification", SendNotificationView.as_view(), name="send_notification"),
    path("view_notification", NotificationView.as_view(), name="view_notification"),
    path("view_appointment", ViewAppointmentView.as_view(), name="view_appointment"),
    path("view_prescription", ViewPrescriptionView.as_view(), name="view_prescription"),
    path('AcceptAppointment/<int:id>/', AcceptAppointment.as_view(), name='AcceptAppointment'),
    path('RejectAppointment/<int:id>/', RejectAppointment.as_view(), name='RejectAppointment'),
    # path('family_history/<int:id>/',familyHistoryView.as_view(), name='family_history'),
    path("view_post", ViewPostView.as_view(), name="view_post"),
    path('add_post', AddPostView.as_view(), name='add_post'),
    path('edit_post/<int:id>/', EditPostView.as_view(), name='edit_post'),
    path('delete_post/<int:id>/', DeletePost.as_view(), name='delete_post'),



####################################################################################################################################


    path('pharmacist_home', PharmacistHomeView.as_view(), name='pharmacist_home'),
    path('Register',RegisterView.as_view(), name='Register'),
    path('add_medicine',AddMedicineView.as_view(), name='add_medicine'),
    path('view_medicine',ManageMedicineView.as_view(), name='view_medicine'),
    path('update_medicine/<int:id>/', UpdateMedicine.as_view(), name='update_medicine'),
    path('delete_medicine/<int:id>/', DeleteMedicine.as_view(), name='delete_medicine'),
    path('profile',PharmacistProfileView.as_view(), name='profile'),
    path('update-order/<int:order_id>/<str:status>/', update_order_status, name='update_order_status'),


# //////////////////////////////  API  ///////////////////////////////


    path('api/register/', UserRegApiView.as_view(), name='register'),
    path('api/login/', loginApiView.as_view(), name='login'),
    path('api/doctors/', ViewDoctorAPI.as_view(), name='doctors'),
    path('api/appointment/<int:lid>', AppointmentBooking.as_view(), name='doctors'),
    path('api/prescription/<int:lid>', ViewPrescriptionAPI.as_view(), name='doctors'),
    path('api/policy/', GovtPolicyViewAPI.as_view(), name='policy'),
    path('api/post/', PostViewAPI.as_view(), name='post'),
    path('api/pharmacists/', ViewPharmacistsAPI.as_view(), name='post'),
    path('api/appointmenthistory/<int:lid>/', AppointmentHistory.as_view(), name='post'),
    path('api/ordermedicine/<int:lid>/', BookMedicinesAPI.as_view(), name='post'),
    path('api/orderhistory/<int:lid>/', OrderHistoryAPI.as_view(), name='post'),
    path('api/notification/<int:lid>/', NotificationViewAPI.as_view(), name='post'),
    path('api/predict/', PredictGeneticDisorder.as_view(), name='predict_genetic_disorder'),
    path('api/predict1/', PredictGeneticDisorder1.as_view(), name='predict_genetic_disorder1'),
    path('api/feedback/<int:id>/', FeedBackAPi.as_view(), name='feedback'),
    path('api/bot/<int:lid>/', MedicalChatbotAPIView.as_view()),
    path('history/<int:id>/', HistoryView.as_view(), name='history'), 

]

