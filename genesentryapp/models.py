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
    Address=models.TextField(null=True,blank=True)


class MedicineTable(models.Model):
    PharmacyId = models.ForeignKey(PharmacistTable,on_delete=models.CASCADE,null=True,blank=True)
    Name=models.CharField(max_length=100,null=True,blank=True)
    Price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    Quantity=models.IntegerField(null=True,blank=True)
    Stock=models.IntegerField(null=True,blank=True)
    Image=models.ImageField(upload_to='medicine_images/', null=True, blank=True)
    ExpiryDate=models.DateField(null=True,blank=True)
    Company=models.CharField(max_length=100,null=True,blank=True)

class Rating(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    Rating=models.IntegerField(null=True,blank=True)
    Feedback=models.TextField(null=True,blank=True)

class Notification(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
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
    Date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    Token=models.IntegerField(null=True,blank=True)

class PrescriptionTable(models.Model):
    Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    Image=models.FileField(upload_to='prescriptions/', null=True, blank=True)
    duration=models.CharField(max_length=100,null=True,blank=True)
    prescription=models.TextField(null=True,blank=True)
    Date=models.DateField(null=True,blank=True)
    #Medicine=models.TextField(null=True,blank=True)
    #Quantity=models.CharField(max_length=100,null=True,blank=True)

class PostTable(models.Model):
    Docid=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)    
    Title=models.CharField(max_length=100,null=True,blank=True)
    Description=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='add_post/', null=True, blank=True)
    Createdate=models.DateField(null=True,blank=True)

class ReviewTable(models.Model):
    user_id=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    doc_name=models.ForeignKey(DoctorTable,on_delete=models.CASCADE,null=True,blank=True)
    comment=models.TextField(null=True,blank=True)
    rating=models.IntegerField(null=True,blank=True)


class OrderTable(models.Model):
    PharmacyId = models.ForeignKey(PharmacistTable,on_delete=models.CASCADE,null=True,blank=True)
    Perscription = models.FileField(upload_to='Prescription', null=True, blank=True)
    USERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Days = models.CharField(max_length=100, null=True, blank=True)
    Status=models.CharField(max_length=100,null=True,blank=True, default='Pending')
    OrderDate=models.DateField(auto_now_add=True)
    

class HistoryTable(models.Model):
    userid = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    department = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class GeneticPrediction(models.Model):
    # Patient input fields
    USERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    patient_age = models.CharField(max_length=10, null=True, blank=True)
    father_age = models.CharField(max_length=10, null=True, blank=True)
    mother_age = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    genes_mother_side = models.CharField(max_length=50, null=True, blank=True)
    inherited_father = models.CharField(max_length=50, null=True, blank=True)
    maternal_gene = models.CharField(max_length=50, null=True, blank=True)
    paternal_gene = models.CharField(max_length=50, null=True, blank=True)
    blood_cell_count = models.CharField(max_length=20, null=True, blank=True)
    white_blood_cell_count = models.CharField(max_length=20, null=True, blank=True)
    respiratory_rate = models.CharField(max_length=20, null=True, blank=True)
    heart_rate = models.CharField(max_length=20, null=True, blank=True)
    parental_consent = models.CharField(max_length=10, null=True, blank=True)
    follow_up = models.CharField(max_length=20, null=True, blank=True)
    birth_effects = models.CharField(max_length=100, null=True, blank=True)
    folic_acid_intake = models.CharField(max_length=100, null=True, blank=True)
    blood_test_result = models.CharField(max_length=50, null=True, blank=True)
    No_of_previous_abortion = models.CharField(max_length=10, null=True, blank=True)

    # Prediction outputs
    genetic_disorder = models.CharField(max_length=200)
    disorder_subclass = models.CharField(max_length=200)

    # Gemini generated description
    description = models.TextField(null=True, blank=True)

    # PDF file path
    report_pdf = models.FileField(upload_to='reports/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.genetic_disorder} - {self.disorder_subclass}"
    
    # class FamilyHistory(models.Model):
    # Userid=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)    
    # History = models.FileField(upload_to='family_history/', null=True, blank=True)

