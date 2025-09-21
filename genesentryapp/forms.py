
from genesentryapp.models import *
from django.forms import ModelForm


class DoctorForm(ModelForm):
    class Meta:
        model = DoctorTable
        fields = ['Name', 'Email', 'Age', 'Gender', 'Qualification', 'Experience', 'Department', 'Phoneno']

class PharmacistForm(ModelForm):
    class Meta:
        model = PharmacistTable
        fields = ['Name', 'Email', 'Age', 'Gender', 'Qualification', 'Phoneno']

class MedicineForm(ModelForm):
    class Meta:
        model = MedicineTable
        fields = ['Name', 'Price', 'Quantity','Stock','Image','ExpiryDate']
    
class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['Rating', 'Feedback']

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['Description','Title','Userid','Date']

class BookmedicineForm(ModelForm):
    class Meta:
        model = BookmedicineTable
        fields = ['Quantity', 'Date']

class GovtPolicyForm(ModelForm):
    class Meta:
        model = GovtPolicyTable
        fields = ['PolicyName', 'file']

class AppointmentForm(ModelForm):
    class Meta:
        model = AppointmentTable
        fields = ['Department', 'Date', 'status', 'Token'] 

class PrescriptionForm(ModelForm):
    class Meta:
        model = PrescriptionTable
        fields = ['prescription','Date', 'Userid']

class PostForm(ModelForm):
    class Meta:
        model = PostTable
        fields = ['Title', 'Description', 'image', 'Createdate']