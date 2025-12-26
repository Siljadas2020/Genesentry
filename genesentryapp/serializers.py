from genesentryapp.models import *
from rest_framework import serializers

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = LoginTable
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorTable
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTable
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='Docid.Name')
    doctor_dept = serializers.CharField(source='Docid.Department')
    class Meta:
        model = PrescriptionTable
        fields = ['Image', 'duration', 'prescription', 'Date', 'doctor_name', 'doctor_dept']


class GovtSerializer(serializers.ModelSerializer):
    class Meta:
        model=GovtPolicyTable
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostTable
        fields = '__all__'

class AppointmentHistorySerializer(serializers.ModelSerializer):
    doc_name=serializers.CharField(source="Docid.Name")
    doc_dept=serializers.CharField(source="Docid.Department")
    class Meta:
        model=AppointmentTable
        fields = ['Date', 'status', 'Token', 'doc_name', 'doc_dept', 'Docid']
        

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model=PharmacistTable
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderTable
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    doctorname = serializers.CharField(source='Docid.Name')
    class Meta:
        model=Notification
        fields = ['Description', 'Date', 'Title', 'doctorname']

class OrderHistory(serializers.ModelSerializer):
    PharmacyName = serializers.CharField(source='PharmacyId.Name')
    class Meta:
        model = OrderTable
        fields = ['Perscription', 'Description', 'Days', 'Status', 'OrderDate', 'PharmacyName']



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields = '__all__'