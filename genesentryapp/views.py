from django.shortcuts import render, HttpResponse
from django.views import View

from genesentryapp.forms import *
from genesentryapp.models import *

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'administration/login.html')
    def post(self,request):
        username=request.POST['Username']
        password=request.POST['Password']
        try:
            user=LoginTable.objects.get(Username=username,Passsword=password)
            request.session['loginid']=user.id
            if user.Userrole=='admin':
                return render(request, 'administration/admin_home.html ')
            elif user.Userrole=='doctor':
                return render(request, 'Doctor/appointments.html')
            elif user.Userrole=='pharmacist':
                return render(request, 'Pharmacy/add.html')
        except LoginTable.DoesNotExist:
            return render(request, 'administration/login.html',{'error':'Invalid username or password'})
        


class AdminHomeView(View):
    def get(self, request):
        return render(request, 'administration/admin_home.html')
    
class AddDoctorView(View):
    def get(self, request):
        return render(request, 'administration/add_doc.html')
    def post(self,request):
        c=DoctorForm(request.POST)
        if c.is_valid():
            reg=c.save(commit=False)
            reg.Loginid=LoginTable.objects.create(Username=reg.Email,Passsword=request.POST['Password'],Userrole='Doctor')
            reg.save()
            return HttpResponse('''<script>alert('Doctor added succesfully!');window.location='/manage_doctors'</script>''')
    
class GovtPolicyView(View):
    def get(self, request):
        return render(request, 'administration/govt_policy.html')

class ManageDoctorsView(View):
    def get(self, request):
        c=DoctorTable.objects.all()
        return render(request, 'administration/manage_doctors.html',{'doctors':c})

class UpdateDocView(View):
    def get(self, request):
        return render(request, 'administration/update_doc.html')

class VerifyPharmacistView(View):
    def get(self, request):
        return render(request, 'administration/verify_pharmacist.html')

class ViewAppointmentsView(View):
    def get(self, request):
        return render(request, 'administration/view_appointments.html')

class ViewPatientsView(View):
    def get(self, request):
        return render(request, 'administration/view_patients.html')

class ViewReviewView(View):
    def get(self, request):
        return render(request, 'administration/view_review.html')

            ######################################################## Doctor #######################################################


class AppointmentsView(View):
    def get(self, request):
        return render(request, 'Doctor/appointments.html')

class MedicalPostsView(View):
    def get(self, request):
        return render(request, 'Doctor/medicalposts.html')

class NotificationView(View):
    def get(self, request):
        return render(request, 'Doctor/notification.html')
    
class PrescriptionView(View):
    def get(self, request):
        return render(request, 'Doctor/prescription.html')  
    
######################################################Pharmacy###########################################################


    
class AddView(View):
    def get(self, request):
        return render(request, 'Pharmacy/add.html')
    
class EditView(View):
    def get(self, request):
        return render(request, 'Pharmacy/edit.html')
    
class ManageMedicineView(View):
    def get(self, request):
        return render(request, 'Pharmacy/manage_medicine.html')
    
class RegisterView(View):
    def get(self, request):
        return render(request, 'Pharmacy/register.html')
    
class RequestView(View):
    def get(self, request):
        return render(request, 'Pharmacy/request.html')