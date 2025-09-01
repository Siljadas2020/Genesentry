from django.db import models

# Create your models here.
class LoginTable(models.Model):
    Username=models.CharField(max_length=100,null=True,blank=True)
    Passsword=models.CharField(max_length=100,null=True,blank=True)
    Userrole=models.CharField(max_length=100,null=True,blank=True)

class UserTable(models.Model):
    Loginid=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Age=models.IntegerField(null=True,blank=True)
    Dob=models.DateField(null=True,blank=True)
    Gender=models.CharField(max_length=10,null=True,blank=True)
    Phoneno=models.CharField(max_length=15,null=True,blank=True)

class DoctorTable(models.Model):
    Loginid=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)  
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Age=models.IntegerField(null=True,blank=True)    
    Gender=models.CharField(max_length=10,null=True,blank=True)
    Department=models.CharField(max_length=100,null=True,blank=True)
    Qualification=models.CharField(max_length=100,null=True,blank=True) 
    Experience=models.IntegerField(null=True,blank=True)
    Phoneno=models.CharField(max_length=15,null=True,blank=True)
    
class PharmacistTable(models.Model):
    Loginid=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Email=models.EmailField(max_length=100,null=True,blank=True)
    Age=models.IntegerField(null=True,blank=True)
    Gender=models.CharField(max_length=10,null=True,blank=True)
    Phoneno=models.CharField(max_length=15,null=True,blank=True)
    Qualification=models.CharField(max_length=100,null=True,blank=True)


class MedicineTable(models.Model):
    PharmacyId = models.ForeignKey(PharmacistTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    Quantity=models.IntegerField(null=True,blank=True)

class Rating(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    Rating=models.IntegerField(null=True,blank=True)
    Feedback=models.TextField(null=True,blank=True)

class Notification(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    Title=models.CharField(max_length=100,null=True,blank=True)

class BookmedicineTable(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True) 
    Medicineid=models.ForeignKey(MedicineTable,on_delete=models.CASCADE,null=True,blank=True)
    Quantity=models.IntegerField(null=True,blank=True)
    Date=models.DateField(null=True,blank=True)

class GovtPolicyTable(models.Model):
    PolicyName=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='govt_policies/', null=True, blank=True)

class AppointmentTable(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    Department=models.CharField(max_length=100,null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    Token=models.IntegerField(null=True,blank=True)

class PrescriptionTable(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    prescription=models.TextField(null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    Medicine=models.TextField(null=True,blank=True)
    Quantity=models.CharField(max_length=100,null=True,blank=True)

class PostTable(models.Model):
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)    
    Title=models.CharField(max_length=100,null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='posts/', null=True, blank=True)
    Createdate=models.DateField(null=True,blank=True)



    





     
