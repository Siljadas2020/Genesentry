from django.shortcuts import redirect, render, HttpResponse
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
            elif user.Userrole=='Doctor':
                return redirect('doctor_home')
            elif user.Userrole=='Pharmacist':
                return redirect('pharmacist_home')
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
    def post(self, request):
        c=GovtPolicyForm(request.POST,request.FILES)
        if c.is_valid():
            c.save()
        return HttpResponse('''<script>alert('Policy added succesfully!');window.location='/view_govt'</script>''')

class ViewGovt(View):
    
    def get(self,request):
        govt=GovtPolicyTable.objects.all()
        return render(request, 'administration/view_govt.html',{'govt':govt})
    
class ViewGovtPolicy(View):
    def get(self, request, id):
        c=GovtPolicyTable.objects.get(id=id)
        return render(request, 'administration/view_govt_policy.html',{'govt':c})
    
class UpdateGovt(View):
    def get(self, request,id):
        c=GovtPolicyTable.objects.get(id=id)
        return render(request, 'administration/update_govt.html',{'govt':c})
    def post(self, request, id):
        c=GovtPolicyTable.objects.get(id=id)
        form=GovtPolicyForm(request.POST,request.FILES, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('Policy updated succesfully!');window.location='/view_govt'</script>''')
        return render(request, 'administration/update_govt.html',{'govt':c,'form':form})
    
class DeleteGovt(View):
    def get(self,request,id):
        c=GovtPolicyTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Policy deleted succesfully!');window.location='/view_govt'</script>''')


class ManageDoctorsView(View):
    def get(self, request):
        c=DoctorTable.objects.all()
        return render(request, 'administration/manage_doctors.html',{'doctors':c})
    

class UpdateDocView(View):
    def get(self, request,id):
        c=DoctorTable.objects.get(id=id)
        return render(request, 'administration/update_doc.html',{'doctor':c})
    def post(self, request, id):
        c=DoctorTable.objects.get(id=id)
        form=DoctorForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('Doctor updated succesfully!');window.location='/manage_doctors'</script>''')
        return render(request, 'administration/update_doc.html',{'doctor':c,'form':form})

class DeleteDocView(View):
    def get(self,request,id):
        c=LoginTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Doctor deleted succesfully!');window.location='/manage_doctors'</script>''')

class ManagePrescriptionView(View):
    def get(self, request):
        c=AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/manage_prescription.html',{'users':c})      
    def post(self,request):
        c=PrescriptionForm(request.POST)
        d = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
        if c.is_valid():
            reg = c.save(commit=False)
            reg.Docid = d
            reg.save()
            return HttpResponse('''<script>alert('Prescription added succesfully!');window.location='/view_prescription'</script>''')    
        
class AcceptAppointment(View):
    def get(self,request,id):
        c=AppointmentTable.objects.get(id=id)
        c.status='Accepted'
        c.save()
        return HttpResponse('''<script>alert('Appointment accepted succesfully!');window.location='/view_appointment'</script>''')
    
class RejectAppointment(View):
    def get(self,request,id):
        c=AppointmentTable.objects.get(id=id)
        c.status='Rejected'
        c.save()
        return HttpResponse('''<script>alert('Appointment rejected succesfully!');window.location='/view_appointment'</script>''')
    
class ViewRatingView(View):
    def get(self, request):
        c=ReviewTable.objects.all()
        return render(request, 'Doctor/view_rating.html',{'rating':c})
    
class NotificationView(View):
    def get(self, request):
      c=Notification.objects.filter(Docid__Loginid__id=request.session['loginid'])
      return render(request, 'Doctor/view_notification.html',{'notification':c})

    
class SendNotificationView(View):
    def get(self, request):
        c=AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/send_notification.html',{'users':c}) 
    def post(self,request):
        print('========================>',request.POST)
        c=NotificationForm(request.POST)
        d = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
        if c.is_valid():
            reg = c.save(commit=False)
            reg.Docid = d
            reg.save()
            return HttpResponse('''<script>alert('Notification sent succesfully!');window.location='/view_notification'</script>''')    

# class NotificationView(View):
#     def get(self, request):
#         return render(request, 'Doctor/send_notification.html')
#     def post(self,request):
#         c=NotificationForm(request.POST)
#         d = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
#         if c.is_valid():
#             reg = c.save(commit=False)
#             reg.Userid = d
#             reg.save()
#             return HttpResponse('''<script>alert('Notification sent succesfully!');window.location='/send_notification'</script>''')
    
    
class ViewAppointmentView(View):
    def get(self, request):
        c=AppointmentTable.objects.all()
        return render(request, 'Doctor/view_appointment.html',{'appointments':c})
    
class ViewPrescriptionView(View):
    def get(self, request):
        c=PrescriptionTable.objects.all()
        return render(request, 'Doctor/view_prescription.html',{'prescriptions':c})

             ######################################################## Administration #######################################################

    

class VerifyPharmacistView(View):
    def get(self, request):
        c=PharmacistTable.objects.all()
        return render(request, 'administration/verify_pharmacist.html',{'pharmacist':c})
    
class  AcceptPharmacist(View):
    def get(self,request,id):
        c=PharmacistTable.objects.get(id=id)
        c.Loginid.Userrole='Pharmacist'
        c.Loginid.save()
        return HttpResponse('''<script>alert('Pharmacist verified succesfully!');window.location='/verify_pharmacist'</script>''')
    
class RejectPharmacist(View):
    def get(self,request,id):
        c=PharmacistTable.objects.get(id=id)
        c.Loginid.Userrole='Rejected'
        c.Loginid.save()
        return HttpResponse('''<script>alert('Pharmacist rejected succesfully!');window.location='/verify_pharmacist'</script>''')
    

class ViewAppointmentsView(View):
    def get(self, request):
        c=AppointmentTable.objects.all()
        return render(request, 'administration/view_appointments.html',{'appointments':c})

class ViewPatientsView(View):
    def get(self, request):
        c=UserTable.objects.all()
        return render(request, 'administration/view_patients.html',{'patients':c})

class ViewReviewView(View):
    def get(self, request):
        c=ReviewTable.objects.all()
        return render(request, 'administration/view_review.html',{'review':c})

            ######################################################## Doctor #######################################################


class AppointmentsView(View):
    def get(self, request):
        return render(request, 'Doctor/appointments.html')

class MedicalPostsView(View):
    def get(self, request):
        return render(request, 'Doctor/medicalposts.html')


class PrescriptionView(View):
    def get(self, request):
        return render(request, 'Doctor/prescription.html')  
    def post(self,request):
        c=PrescriptionForm(request.POST)
        if c.is_valid():
            c.save()
            return HttpResponse('''<script>alert('Prescription added succesfully!');window.location='/view_prescription'</script>''')
        
class UpdatePrescription(View):
    def get(self, request,id):
        c=PrescriptionTable.objects.get(id=id)
        d = AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/update_prescription.html',{'prescription':c, 'users':d})
    def post(self, request, id):
        c=PrescriptionTable.objects.get(id=id)
        form=PrescriptionForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('Prescription updated succesfully!');window.location='/view_prescription'</script>''')
        return render(request, 'Doctor/update_prescription.html',{'prescription':c,'form':form})

class DeletePrescription(View):
    def get(self,request,id):
        c=PrescriptionTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Prescription deleted succesfully!');window.location='/view_prescription'</script>''')
    
class DoctorHomeView(View):
    def get(self, request):
        return render(request, 'Doctor/doctor_home.html')
    

######################################################Pharmacy###########################################################


class PharmacistHomeView(View):
    def get(self, request):
        return render(request, 'pharmacy/pharmacist_home.html')

class AddMedicineView(View):
    def get(self, request):
        return render(request, 'pharmacy/add_medicine.html')
    def post(self, request):
        c = MedicineForm(request.POST, request.FILES)
        d = PharmacistTable.objects.get(Loginid__id=request.session['loginid'])

        if c.is_valid():
            reg = c.save(commit=False)
            reg.PharmacyId = d
            reg.save()
            return HttpResponse('''<script>alert('Medicine added successfully!');window.location='/view_medicine'</script>''')
        else:
            return render(request, 'pharmacy/add_medicine.html', {'form': c})
        
class ManageMedicineView(View):
    def get(self, request):
        c=MedicineTable.objects.all()
        return render(request, 'pharmacy/view_medicine.html',{'medicine':c})
        
class DeleteMedicine(View):
    def get(self,request,id):
        c=MedicineTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Medicine deleted succesfully!');window.location='/view_medicine'</script>''')
    
class UpdateMedicine(View):
    def get(self, request,id):
        c=MedicineTable.objects.get(id=id)
        return render(request, 'pharmacy/update_medicine.html',{'medicine':c})
    def post(self, request, id):
        c=MedicineTable.objects.get(id=id)
        form=MedicineForm(request.POST,request.FILES, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('Medicine updated succesfully!');window.location='/view_medicine'</script>''')
        return render(request, 'pharmacy/update_medicine.html',{'medicine':c,'form':form})

class AddPostView(View):
    def get(self, request):
            return render(request, 'Doctor/add_post.html')
    def post(self,request):
        c=PostForm(request.POST,request.FILES)
        if c.is_valid():
            reg = c.save(commit=False)
            d = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
            reg.Doctorid=d
            reg.save()
            return HttpResponse('''<script>alert('Post added succesfully!');window.location='/view_post'</script>''')

class ViewPostView(View):
    def get(self, request):
        c=PostTable.objects.all()
        return render(request, 'Doctor/view_post.html',{'post':c})

class EditPostView(View):
    def get(self, request,id):
        c=PostTable.objects.get(id=id)
        return render(request, 'Doctor/edit_post.html',{'post':c})
    def post(self, request,id):
        c=PostTable.objects.get(id=id)
        form=PostForm(request.POST,request.FILES, instance=c)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert('Post updated succesfully!');window.location='/view_post'</script>''')
        return render(request, 'Doctor/edit_post.html',{'post':c,'form':form})
    
class DeletePost(View):
    def get(self,request,id):
        c=PostTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Post deleted succesfully!');window.location='/view_post'</script>''')

class AddView(View):
    def get(self, request):
    
        return render(request, 'Pharmacy/add.html')
    
class EditView(View):
    def get(self, request):
        return render(request, 'Pharmacy/edit.html')
    
# class ManageMedicineView(View):
    # def get(self, request):
        # return render(request, 'Pharmacy/manage_medicine.html')
    
    
class RegisterView(View):
    def get(self, request):
        return render(request, 'Pharmacy/register.html')
    def post(self,request):
        c=PharmacistForm(request.POST)
        if c.is_valid():
            reg=c.save(commit=False)
            reg.Loginid=LoginTable.objects.create(Username=reg.Email,Passsword=request.POST['Password'],Userrole='Pending')
            reg.save()
            return HttpResponse('''<script>alert('Pharmacist added succesfully!');window.location='/verify_pharmacist'</script>''')




    
class RequestView(View):
    def get(self, request):
        return render(request, 'Pharmacy/request.html')