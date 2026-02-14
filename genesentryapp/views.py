from django.shortcuts import redirect, render, HttpResponse
from django.views import View

from genesentryapp.forms import *
from genesentryapp.models import *
from rest_framework import status


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

class LogoutView(View):
    def get(self, request):
        try:
            del request.session['loginid']
        except KeyError:
            pass
        return HttpResponse('''<script>alert("Logged out successfully!");window.location="/"</script>''')

class AdminHomeView(View):
    def get(self, request):
        c = DoctorTable.objects.count()
        d = UserTable.objects.count()
        e = PharmacistTable.objects.count()
        f = GovtPolicyTable.objects.count()
        return render(request, 'administration/admin_home.html',{'doctor_count':c, 'patient_count':d, 'pharmacist_count':e, 'govt_policy_count':f})

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

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import PrescriptionTable, DoctorTable, AppointmentTable, UserTable
from .forms import PrescriptionForm
from reportlab.pdfgen import canvas
from django.core.files import File
import os
from django.conf import settings

class ManagePrescriptionView(View):
    def get(self, request):
        c = AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
        user_obj = UserTable.objects.all()
        return render(request, 'Doctor/manage_prescription.html', {'users': c, 'user_obj': user_obj})

    def post(self, request):
        form = PrescriptionForm(request.POST)
        d = DoctorTable.objects.get(Loginid_id=request.session['loginid'])
        if form.is_valid():
            reg = form.save(commit=False)
            reg.Docid = d
            reg.save()

            # ---- Generate PDF from prescription text ----
            prescription_text = reg.prescription or "No prescription text provided"
            pdf_filename = f"prescription_{reg.id}.pdf"
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'prescriptions', pdf_filename)

            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            # Create the PDF
            c = canvas.Canvas(pdf_path)
            c.setFont("Helvetica", 12)
            textobject = c.beginText(50, 800)
            textobject.textLine("Prescription")
            textobject.textLine("====================")
            textobject.textLines(prescription_text)
            c.drawText(textobject)
            c.showPage()
            c.save()

            # Save PDF to FileField
            with open(pdf_path, 'rb') as f:
                reg.Image.save(pdf_filename, File(f), save=True)

            return HttpResponse(
                '''<script>alert("Prescription added successfully!");window.location='/view_prescription'</script>'''
            )

        return HttpResponse(
            '''<script>alert("Invalid form submission!");window.location='/manage_prescription'</script>'''
        )
    
        
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
        c=Rating.objects.filter(Docid__Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/view_rating.html',{'rating':c})
    
class NotificationView(View):
    def get(self, request):
      c=Notification.objects.filter(Docid__Loginid__id=request.session['loginid'])
      return render(request, 'Doctor/view_notification.html',{'notification':c})

    
class SendNotificationView(View):
    def get(self, request):
        # Fetch all appointments for the logged-in doctor
        appointments = AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/send_notification.html', {'user_obj': appointments})
    
    def post(self, request):
        print('POST DATA:', request.POST)  # Debug print
        
        form = NotificationForm(request.POST)
        doctor = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
        
        if form.is_valid():
            notification = form.save(commit=False)
            notification.Docid = doctor
            notification.save()
            return HttpResponse(
                '''<script>
                    alert('Notification sent successfully!');
                    window.location='/view_notification';
                </script>'''
            )
        else:
            print("Form errors:", form.errors)
            return HttpResponse(
                '''<script>
                    alert('Error sending notification!');
                    window.history.back();
                </script>'''
            )    

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
        c=AppointmentTable.objects.filter(Docid__Loginid__id=request.session['loginid'])
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
        c=Rating.objects.all()
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
            reg = form.save(commit=False)
             # ---- Generate PDF from prescription text ----
            prescription_text = reg.prescription or "No prescription text provided"
            pdf_filename = f"prescription_{reg.id}.pdf"
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'prescriptions', pdf_filename)

            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

            # Create the PDF
            c = canvas.Canvas(pdf_path)
            c.setFont("Helvetica", 12)
            textobject = c.beginText(50, 800)
            textobject.textLine("Prescription")
            textobject.textLine("====================")
            textobject.textLines(prescription_text)
            c.drawText(textobject)
            c.showPage()
            c.save()

            # Save PDF to FileField
            with open(pdf_path, 'rb') as f:
                reg.Image.save(pdf_filename, File(f), save=True)
            return HttpResponse('''<script>alert('Prescription updated succesfully!');window.location='/view_prescription'</script>''')
        return render(request, 'Doctor/update_prescription.html',{'prescription':c,'form':form})

class DeletePrescription(View):
    def get(self,request,id):
        c=PrescriptionTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Prescription deleted succesfully!');window.location='/view_prescription'</script>''')
    
class DoctorHomeView(View):
    def get(self, request):
        c = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
        return render(request, 'Doctor/doctor_home.html',{'doctor':c})
    

######################################################Pharmacy###########################################################


class PharmacistHomeView(View):
    def get(self, request):
        return render(request, 'pharmacy/pharmacist_home.html')
    
class PharmacistProfileView(View):
    def get(self, request):
        c=PharmacistTable.objects.get(Loginid__id=request.session['loginid'])
        return render(request, 'pharmacy/profile.html',{'pharmacist':c})
    

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
        d = DoctorTable.objects.get(Loginid__id=request.session['loginid'])
        print(d)
        c=PostForm(request.POST,request.FILES)
        if c.is_valid():
            reg = c.save(commit=False)
            reg.Docid=d
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
            return HttpResponse('''<script>alert('Pharmacist added succesfully!');window.location='/'</script>''')




    
class RequestView(View):
    def get(self, request):
        return render(request, 'Pharmacy/request.html')
    

class NewPrescriptionView(View):
    def get(self, request):
        c=PrescriptionTable.objects.all()
        return render(request, 'pharmacy/newprescription.html',{'prescriptions':c})
    
class AcceptPrescription(View):
    def get(self,request,id):
        c=PrescriptionTable.objects.get(id=id)
        c.status='Accepted'
        c.save()
        return HttpResponse('''<script>alert('Prescription accepted succesfully!');window.location='/new_prescription'</script>''')

class RejectPrescription(View):
    def get(self,request,id):
        c=PrescriptionTable.objects.get(id=id)
        c.status='Rejected'
        c.save()
        return HttpResponse('''<script>alert('Prescription rejected succesfully!');window.location='/new_prescription'</script>''')
    
class StatusView(View):
    def get(self, request):
        return render(request, 'pharmacy/status.html')
    
# class OrderView(View):
#     def get(self, request):
#         c=OrderTable.objects.all()
#         return render(request, 'pharmacy/order.html',{'orders':c})
#     def post(self,request):
#         c=orderTableForm(request.POST)
#         d = PharmacistTable.objects.get(Loginid__id=request.session['loginid'])
#         if c.is_valid():
#             reg = c.save(commit=False)
#             reg.PharmacyId = d
#             reg.save()
#             return HttpResponse('''<script>alert('Order placed succesfully!');window.location='/view_order'</script>''')
    
    
class ViewOrder(View):
    def get(self, request):
        c=OrderTable.objects.filter(PharmacyId__Loginid__id = request.session['loginid'])
        return render(request, 'pharmacy/view_order.html',{'orders':c})
    

class DeleteOrder(View):
    def get(self,request,id):
        c=OrderTable.objects.get(id=id)
        c.delete()
        return HttpResponse('''<script>alert('Order deleted succesfully!');window.location='/view_order'</script>''')
    


# //////////////////////////////////  API  ////////////////////////////////////////////


from genesentryapp.serializers import *
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.response import Response

class UserRegApiView(APIView):
    def post(self,request):
        print('==================',request.data)
        reg_serial=UserSerializer(data=request.data)
        login_serial=LoginSerializers(data=request.data)

        regvalid=reg_serial.is_valid()
        loginvalid=login_serial.is_valid()  

        if regvalid and loginvalid:
            login=login_serial.save(Userrole='User')
            reg_serial.save(Loginid=login)
            return Response({'message':'Registration successful'},status=HTTP_200_OK)
        else:
            return Response({'Registration error': reg_serial.errors if not regvalid else None,
                             'login error': login_serial.errors if not loginvalid else None}, status=HTTP_400_BAD_REQUEST)
        
class loginApiView(APIView):
    def post(self,request):
        Response_dict={}
        Username=request.data.get('Username')
        Password=request.data.get('Password')
        try:
            if not Username or not Password:
                return Response({'Response': 'Login failed'}, status=HTTP_400_BAD_REQUEST)
            uname=LoginTable.objects.filter(Username=Username, Passsword=Password).first()
            if not uname:
                return Response({'Response':'login failed!'}, status=HTTP_400_BAD_REQUEST)
            else:
                Response_dict['message'] = 'login successful'
                Response_dict['UserType'] = uname.Userrole
                Response_dict['userid'] = uname.id
                return Response(Response_dict,status=HTTP_200_OK)
        except Exception as e:
            return Response({'Response':'internal server error'},status=HTTP_500_INTERNAL_SERVER_ERROR)
        
from django.db.models import Avg

        

class ViewDoctorAPI(APIView):
    def get(self, request):
        doctors = DoctorTable.objects.all()
        serializer = DoctorSerializer(doctors, many=True)

        doctor_data = []
        for doc in serializer.data:
            doc_id = doc['id']  # assuming 'id' is present in DoctorSerializer

            # Get all ratings for this doctor
            ratings = Rating.objects.filter(Docid_id=doc_id)

            # Average rating
            avg_rating = ratings.aggregate(Avg('Rating'))['Rating__avg']
            doc['average_rating'] = round(avg_rating, 2) if avg_rating else None

            # All feedbacks (non-empty)
            feedbacks = list(ratings.values_list('Feedback', flat=True))
            doc['feedbacks'] = [fb for fb in feedbacks if fb]

            doctor_data.append(doc)

        return Response(doctor_data, status=HTTP_200_OK)
    
class AppointmentBooking(APIView):
    def post(self, request, lid):
        print(request.data)
        try:
            c = UserTable.objects.get(Loginid__id=lid)
        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            date = serializer.validated_data.get("Date")
            if not date:
                return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

            existing_count = AppointmentTable.objects.filter(Date=date).count()

            next_token = existing_count + 1

            appointment = serializer.save(Userid=c, status="pending", Token=next_token)

            return Response({
                "message": "Appointment booked successfully",
                "appointment_id": appointment.id,
                "date": str(date),
                "token": next_token,
                "status": appointment.status
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewPrescriptionAPI(APIView):
    def get(self, request, lid):
        c = PrescriptionTable.objects.filter(Userid__Loginid__id = lid)
        d = PrescriptionSerializer(c, many=True)
        print(d.data)
        return Response(d.data, status=HTTP_200_OK)
    

class GovtPolicyViewAPI(APIView):
    def get(self, request):
        c = GovtPolicyTable.objects.all()
        serializer = GovtSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

class PostViewAPI(APIView):
    def get(self, request):
        c = PostTable.objects.all()
        serializer = PostSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class AppointmentHistory(APIView):
    def get(self, request, lid):
        c = AppointmentTable.objects.filter(Userid__Loginid__id = lid)
        d=AppointmentHistorySerializer(c, many=True)
        return Response(d.data, status=HTTP_200_OK)

class ViewPharmacistsAPI(APIView):
    def get(self, request):
        c = PharmacistTable.objects.all()
        serializer = PharmacistSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class BookMedicinesAPI(APIView):
    def post(self, request, lid):
        print(request.data)
        c = UserTable.objects.get(Loginid_id = lid)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(USERID=c, Status="Pending")
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.error, status=HTTP_400_BAD_REQUEST)
    
from django.shortcuts import get_object_or_404, redirect
    
def update_order_status(request, order_id, status):
    """
    Update the status of an order to Accepted or Rejected
    """
    order = get_object_or_404(OrderTable, id=order_id)
    
    if status in ['Accepted', 'Rejected']:
        order.Status = status
        order.save()
        print(f"Order {order.id} status updated to {status}") 
    
    return redirect('view_order')  

class OrderHistoryAPI(APIView):
    def get(self, request, lid):
        c = OrderTable.objects.filter(USERID__Loginid__id = lid)
        serializer = OrderHistory(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class NotificationViewAPI(APIView):
    def get(self, request, lid):
        c = Notification.objects.filter(Userid__Loginid__id = lid)
        serializer = NotificationSerializer(c, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from reportlab.pdfgen import canvas
from django.conf import settings
import pandas as pd
import numpy as np
import os
import traceback

# ===================================================
# GEMINI API CONFIGURATION
# ===================================================
import google.generativeai as genai
genai.configure(api_key="AIzaSyAkQVzfbNuM1iS7ZcgWVYe61v4cHtaRM7c")  

from .models import GeneticPrediction

# ===================================================
# ML MODELS (LOAD + TRAIN)
# ===================================================
print("🔹 Loading dataset...")

try:
    train_df = pd.read_csv("genesentryapp/data/train.csv")
except FileNotFoundError:
    print("❌ train.csv not found in genesentryapp/data/")
    raise

selected_columns = [
    'Patient Age',
    "Genes in mother's side",
    'Inherited from father',
    'Maternal gene',
    'Paternal gene',
    'Blood cell count (mcL)',
    "Mother's age",
    "Father's age",
    'Respiratory Rate (breaths/min)',
    'Heart Rate (rates/min)',
    'Parental consent',
    'Follow-up',
    'Gender',
    'Birth defects',
    'Folic acid details (peri-conceptional)',
    'No. of previous abortion',
    'White Blood cell count (thousand per microliter)',
    'Blood test result',
    'Genetic Disorder',
    'Disorder Subclass'
]

train_df = train_df[[c for c in selected_columns if c in train_df.columns]].copy()
train_df.replace('-', np.nan, inplace=True)
train_df.fillna(train_df.mode().iloc[0], inplace=True)

X = train_df.drop(columns=['Genetic Disorder', 'Disorder Subclass'])
y_genetic = train_df['Genetic Disorder']
y_subclass = train_df['Disorder Subclass']

X_encoded = pd.get_dummies(X)

from sklearn.ensemble import RandomForestClassifier

print("🔹 Training models...")

model_genetic = RandomForestClassifier(n_estimators=100, random_state=42)
model_genetic.fit(X_encoded, y_genetic)

model_subclass = RandomForestClassifier(n_estimators=100, random_state=42)
model_subclass.fit(X_encoded, y_subclass)

print("✅ Models trained successfully!")

# ===================================================
# API VIEW WITH GEMINI + PDF GENERATION
# ===================================================
class PredictGeneticDisorder1(APIView):

    column_map = {
        "patient_age": "Patient Age",
        "father_age": "Father's age",
        "Mother_age": "Mother's age",
        "gender": "Gender",
        "genes_mother_side": "Genes in mother's side",
        "inherited_father": "Inherited from father",
        "maternal_gene": "Maternal gene",
        "paternal_gene": "Paternal gene",
        "blood_cell_count": "Blood cell count (mcL)",
        "white_blood_cell_count": "White Blood cell count (thousand per microliter)",
        "respiratory_rate": "Respiratory Rate (breaths/min)",
        "heart_rate": "Heart Rate (rates/min)",
        "parental_consent": "Parental consent",
        "follow_up": "Follow-up",
        "birth_effects": "Birth defects",
        "folic_acid_intake": "Folic acid details (peri-conceptional)",
        "blood_test_result": "Blood test result",
        "No_of_previous_abortion": "No. of previous abortion"
    }

    def post(self, request):
        try:
            print("📩 Received:", request.data)
            input_data = request.data

            # ---------------------------
            # Prepare input for ML model
            # ---------------------------
            mapped_input = {self.column_map[k]: v for k, v in input_data.items() if k in self.column_map}
            df = pd.DataFrame([mapped_input])
            df_encoded = pd.get_dummies(df)
            df_encoded = df_encoded.reindex(columns=X_encoded.columns, fill_value=0)

            # ---------------------------
            # Prediction
            # ---------------------------
            pred_genetic = model_genetic.predict(df_encoded)[0]
            pred_subclass = model_subclass.predict(df_encoded)[0]

            # ---------------------------
            # Gemini AI Description
            # ---------------------------
            prompt = f"""
            Explain the genetic disorder below in simple medical terms.
            Include overview, causes, symptoms, risk factors, treatment, and prevention.

            Disorder: {pred_genetic}
            Subclass: {pred_subclass}
            """
            try:
                gmodel = genai.GenerativeModel("gemini-2.0-flash")
                resp = gmodel.generate_content(prompt)
                description = resp.text.strip()
                if not description:
                    description = "AI description could not be generated."
            except Exception as e:
                print("Gemini API Error:", e)
                description = "AI description could not be generated."  

            # ---------------------------
            # Normalize keys for DB
            # ---------------------------
            normalized_data = {
                "patient_age": input_data.get("patient_age"),
                "father_age": input_data.get("father_age"),
                "mother_age": input_data.get("Mother_age"),
                "gender": input_data.get("gender"),
                "genes_mother_side": input_data.get("genes_mother_side"),
                "inherited_father": input_data.get("inherited_father"),
                "maternal_gene": input_data.get("maternal_gene"),
                "paternal_gene": input_data.get("paternal_gene"),
                "blood_cell_count": input_data.get("blood_cell_count"),
                "white_blood_cell_count": input_data.get("white_blood_cell_count"),
                "respiratory_rate": input_data.get("respiratory_rate"),
                "heart_rate": input_data.get("heart_rate"),
                "parental_consent": input_data.get("parental_consent"),
                "follow_up": input_data.get("follow_up"),
                "birth_effects": input_data.get("birth_effects"),
                "folic_acid_intake": input_data.get("folic_acid_intake"),
                "blood_test_result": input_data.get("blood_test_result"),
                "No_of_previous_abortion": input_data.get("No_of_previous_abortion"),
            }

            userid = input_data.get("userid")
            user_obj = UserTable.objects.get(Loginid__id=userid)

            # ---------------------------
            # Save to Database
            # ---------------------------
            obj = GeneticPrediction.objects.create(
                genetic_disorder=pred_genetic,
                disorder_subclass=pred_subclass,
                description=description,
                USERID=user_obj,
                **normalized_data
            )

            # ---------------------------
            # PDF Generation
            # ---------------------------
            pdf_dir = os.path.join(settings.MEDIA_ROOT, "reports")
            os.makedirs(pdf_dir, exist_ok=True)

            pdf_filename = f"genetic_report_{obj.id}.pdf"
            pdf_path = os.path.join(pdf_dir, pdf_filename)

            c = canvas.Canvas(pdf_path)
            c.setFont("Helvetica", 12)

            text_obj = c.beginText(50, 800)
            text_obj.textLine("GENETIC DISORDER REPORT")
            text_obj.textLine("====================================")
            text_obj.textLine("")
            text_obj.textLine(f"Genetic Disorder: {pred_genetic}")
            text_obj.textLine(f"Subclass: {pred_subclass}")
            text_obj.textLine("")
            text_obj.textLine("----- PATIENT DETAILS -----")

            for k, v in normalized_data.items():
                text_obj.textLine(f"{k}: {v}")

            text_obj.textLine("")
            text_obj.textLine("----- DESCRIPTION -----")
            for line in description.split("\n"):
                text_obj.textLine(line)

            c.drawText(text_obj)
            c.showPage()
            c.save()

            # Attach PDF
            with open(pdf_path, "rb") as pdf:
                obj.report_pdf.save(pdf_filename, File(pdf), save=True)

            # ---------------------------
            # Response
            # ---------------------------
            return Response({
                "Genetic Disorder": pred_genetic,
                "Disorder Subclass": pred_subclass,
                "Description": description,
                "PDF_URL": obj.report_pdf.url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

from genesentryapp.main import predict_disease   # 👈 important

# class PredictGeneticDisorder(APIView):
#     def post(self, request):
#         print("-------------------------------------------------", request.data)
#         print("----------------PredictGeneticDisorder API initialized")
#         print("Received data:", request.data)

#         try:
#             result = predict_disease(request.data)
#             print("Prediction result:----------------", result)
#             return Response(result, status=status.HTTP_200_OK)

#         except Exception as e:
#             traceback.print_exc()
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback
import os
from datetime import datetime

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from openai import OpenAI

# =========================
# OpenRouter Configuration
# =========================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# =========================
# API VIEW
# =========================
# class PredictGeneticDisorder(APIView):
#     def post(self, request):
#         print("-------------------------------------------------", request.data)
#         try:
#             user = UserTable.objects.get(Loginid__id=request.data.get("userid"))

#             # ML prediction
#             result = predict_disease(request.data)
#             disorder = result.get("Predicted Disorder Subclass")

#             # LLM description (OpenRouter)
#             description = generate_disorder_description(disorder, request.data)

#             # Save prediction
#             prediction = GeneticPrediction.objects.create(
#                 USERID=user,
#                 patient_age=request.data.get("patient_age"),
#                 father_age=request.data.get("father_age"),
#                 mother_age=request.data.get("Mother_age"),
#                 gender=request.data.get("gender"),
#                 genes_mother_side=request.data.get("genes_mother_side"),
#                 inherited_father=request.data.get("inherited_father"),
#                 maternal_gene=request.data.get("maternal_gene"),
#                 paternal_gene=request.data.get("paternal_gene"),
#                 blood_cell_count=request.data.get("blood_cell_count"),
#                 white_blood_cell_count=request.data.get("white_blood_cell_count"),
#                 respiratory_rate=request.data.get("respiratory_rate"),
#                 heart_rate=request.data.get("heart_rate"),
#                 parental_consent=request.data.get("parental_consent"),
#                 follow_up=request.data.get("follow_up"),
#                 birth_effects=request.data.get("birth_effects"),
#                 folic_acid_intake=request.data.get("folic_acid_intake"),
#                 blood_test_result=request.data.get("blood_test_result"),
#                 genetic_disorder="Genetic Disorder",
#                 disorder_subclass=disorder,
#                 description=description
#             )

#             # Generate PDF
#             pdf_path = generate_pdf_report(prediction)
#             prediction.report_pdf = pdf_path
#             prediction.save()

#             return Response({
#                 "prediction": disorder,
#                 "description": description,
#                 "pdf": prediction.report_pdf.url
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             traceback.print_exc()
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# =========================
# PDF GENERATION
# =========================
def generate_pdf_report(prediction_obj):
    filename = f"genetic_report_{prediction_obj.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, "reports", filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 40

    def draw(text):
        nonlocal y
        c.drawString(40, y, text)
        y -= 18

    draw("Genetic Disorder Prediction Report")
    draw("-" * 90)

    draw(f"Patient Age: {prediction_obj.patient_age}")
    draw(f"Gender: {prediction_obj.gender}")
    draw(f"Predicted Disorder: {prediction_obj.genetic_disorder}")
    draw(f"Subclass: {prediction_obj.disorder_subclass}")
    draw(f"Date: {datetime.now().strftime('%d-%m-%Y')}")

    y -= 20
    draw("Description:")
    y -= 10

    text_object = c.beginText(40, y)
    for line in prediction_obj.description.split("\n"):
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

    return f"reports/{filename}"

# # =========================
# # OPENROUTER LLM
# # =========================
def generate_disorder_description(disorder_name, patient_data):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a medical assistant generating clear, patient-friendly "
                        "explanations for genetic disorders."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
Explain the genetic disorder "{disorder_name}" in clear, patient-friendly language.

Include:
- Overview
- Causes
- Symptoms
- Diagnosis
- Treatment
- Follow-up advice
"""
                }
            ],
            temperature=0.3,
            max_tokens=500,
        )

        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        print("⚠️ OpenRouter failed. Falling back.")
        print("Reason:", str(e))
        return get_fallback_description(disorder_name)

# # =========================
# # FALLBACK (SAFE MODE)
# # =========================
def get_fallback_description(disorder_name):
    fallback_data = {
        "Leigh syndrome": (
            "Leigh syndrome is a rare inherited neurological disorder that primarily "
            "affects infants and children. It is caused by defects in mitochondrial "
            "energy production.\n\n"
            "Common symptoms include developmental delay, muscle weakness, breathing "
            "difficulties, and neurological deterioration.\n\n"
            "Diagnosis involves clinical evaluation, genetic testing, and imaging. "
            "There is currently no cure, and treatment focuses on symptom management "
            "and supportive care.\n\n"
            "Regular follow-up with neurologists and genetic specialists is recommended."
        )
    }

    return fallback_data.get(
        disorder_name,
        "This genetic disorder requires specialist medical evaluation and follow-up care."
    )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

from .models import UserTable, GeneticPrediction
from .main import predict_disease


class PredictGeneticDisorder(APIView):

    def normalize_inputs(self, data):
        """
        Normalize frontend values → model-friendly values
        """

        respiratory_map = {
            "Normal (30–60)": "Normal",
            "Normal (12–20)": "Normal",
            "High": "High",
            "Low": "Low"
        }

        heart_map = {
            "Tachycardia": "High",
            "Bradycardia": "Low",
            "Normal": "Normal"
        }

        blood_test_map = {
            "Not": "Normal",
            "Abnormal": "Abnormal",
            "Inconclusive": "Inconclusive"
        }

        if "respiratory_rate" in data:
            data["respiratory_rate"] = respiratory_map.get(
                data["respiratory_rate"], data["respiratory_rate"]
            )

        if "heart_rate" in data:
            data["heart_rate"] = heart_map.get(
                data["heart_rate"], data["heart_rate"]
            )

        if "blood_test_result" in data:
            data["blood_test_result"] = blood_test_map.get(
                data["blood_test_result"], data["blood_test_result"]
            )

        return data


    def post(self, request):
        print("Incoming data:", request.data)

        try:
            user_id = request.data.get("userid")
            if not user_id:
                return Response(
                    {"error": "userid is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = UserTable.objects.get(Loginid__id=user_id)

            # ✅ Normalize inputs
            cleaned_data = self.normalize_inputs(request.data.copy())

            # ✅ Predict
            result = predict_disease(cleaned_data)
            disorder = result.get("Predicted Disorder Subclass", "Unknown")

            # ✅ Generate description
            description = generate_disorder_description(disorder, cleaned_data)

            # ✅ Save prediction
            prediction = GeneticPrediction.objects.create(
                USERID=user,
                patient_age=cleaned_data.get("patient_age"),
                father_age=cleaned_data.get("father_age"),
                mother_age=cleaned_data.get("Mother_age"),
                gender=cleaned_data.get("gender"),
                genes_mother_side=cleaned_data.get("genes_mother_side"),
                inherited_father=cleaned_data.get("inherited_father"),
                maternal_gene=cleaned_data.get("maternal_gene"),
                paternal_gene=cleaned_data.get("paternal_gene"),
                blood_cell_count=cleaned_data.get("blood_cell_count"),
                white_blood_cell_count=cleaned_data.get("white_blood_cell_count"),
                respiratory_rate=cleaned_data.get("respiratory_rate"),
                heart_rate=cleaned_data.get("heart_rate"),
                blood_test_result=cleaned_data.get("blood_test_result"),
                genetic_disorder="Genetic Disorder",
                disorder_subclass=disorder,
                description=description
            )

            # ✅ PDF
            pdf_path = generate_pdf_report(prediction)
            prediction.report_pdf = pdf_path
            prediction.save()

            return Response({
                "prediction": disorder,
                "description": description,
                "pdf": prediction.report_pdf.url
            }, status=status.HTTP_200_OK)

        except UserTable.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////


class FeedBackAPi(APIView):
    def post(self, request, id):
        print(request.data)
        c = UserTable.objects.get(Loginid__id = id)
        serializers = RatingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(Userid=c)
            return Response(serializers.data, status=HTTP_200_OK)
        return Response(serializers.error, status=HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

from openai import OpenAI

from .models import UserTable, HistoryTable


# 🔑 OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)


class MedicalChatbotAPIView(APIView):

    # ---------------------- GET CHAT HISTORY ----------------------
    def get(self, request, lid):
        try:
            user = UserTable.objects.get(Loginid__id=lid)
            history = HistoryTable.objects.filter(userid=user).order_by("-timestamp")

            data = [
                {
                    "user_message": h.user_message,
                    "bot_response": h.bot_response,
                    "department": h.department,
                    "time": h.timestamp
                }
                for h in history
            ]

            return Response({"history": data}, status=status.HTTP_200_OK)

        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # ---------------------- POST MESSAGE ----------------------
    def post(self, request, lid):
        user_message = request.data.get("message", "").strip().lower()

        if not user_message:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserTable.objects.get(Loginid__id=lid)

            # -------------------------------
            # CASUAL / POLITE REPLIES
            # -------------------------------
            casual_words = ["ok", "okay", "thanks", "thank you", "tnx", "bye", "good", "nice"]

            if user_message in casual_words:
                bot_response = (
                    "You’re welcome! If you experience any symptoms again or need guidance, "
                    "feel free to message me anytime. Take care."
                )

                HistoryTable.objects.create(
                    userid=user,
                    user_message=user_message,
                    bot_response=bot_response,
                    department="None"
                )

                return Response({
                    "department": "None",
                    "response": bot_response
                }, status=status.HTTP_200_OK)

            # -----------------------------------------
            # NORMAL FLOW → OPENROUTER (GPT)
            # -----------------------------------------
            prompt = f"""
You are a medical assistant chatbot.

The user describes symptoms:
"{user_message}"

Rules:
- Identify the MOST suitable medical department.
- Do NOT diagnose.
- Do NOT prescribe medicines.

Respond EXACTLY in this format:
Department: <department name>
Reason: <short explanation>
"""

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a safe medical triage assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )

                bot_response = response.choices[0].message.content.strip()

            except Exception as e:
                bot_response = "AI service temporarily unavailable."

            # -------------------------------
            # EXTRACT DEPARTMENT
            # -------------------------------
            department_line = "Unknown"

            if "Department:" in bot_response:
                department_line = (
                    bot_response.split("Department:")[1]
                    .split("\n")[0]
                    .strip()
                )

            # -------------------------------
            # SAVE CHAT HISTORY
            # -------------------------------
            HistoryTable.objects.create(
                userid=user,
                user_message=user_message,
                bot_response=bot_response,
                department=department_line
            )

            return Response({
                "department": department_line,
                "response": bot_response
            }, status=status.HTTP_200_OK)

        except UserTable.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )




class HistoryView(View):
    def get(self, request, id):
        c = GeneticPrediction.objects.filter(USERID__id = id) 
        return render(request, 'Doctor/view_history.html',{'history':c})   
    
# class familyHistoryView(View):
#     def get(self, request, id):
#         c = FamilyHistory.objects.filter(USERID__id = id) 
#         return render(request, 'Doctor/family_history.html',{'family_history':c})  

