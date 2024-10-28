from django.db import models

# Create your models here.

class Voter(models.Model):
    VoterID = models.AutoField(primary_key=True)  # Auto-incremented, unique
    government_number = models.BigIntegerField()  # Ensure numeric
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    CNIC = models.BigIntegerField(unique=True)  # CNIC should be numeric and unique
    address = models.TextField()
    mobile_number = models.BigIntegerField()  # Numeric mobile number
    family_code = models.BigIntegerField(null=True, blank=True)
    block_number = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # If family code is not provided, set it to VoterID
        if not self.family_code:
            self.family_code = self.VoterID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (VoterID: {self.VoterID})"