from django.contrib import admin

from genesentryapp.models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(DoctorTable)
admin.site.register(PharmacistTable)
admin.site.register(MedicineTable)
admin.site.register(Rating)
admin.site.register(Notification)
admin.site.register(BookmedicineTable)
admin.site.register(AppointmentTable)
admin.site.register(PrescriptionTable)
admin.site.register(GovtPolicyTable)
admin.site.register(PostTable)
admin.site.register(ReviewTable)
admin.site.register(OrderTable)