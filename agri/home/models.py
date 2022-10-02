from django.db import models
# Create your models here.
class Signup(models.Model):
  username=models.CharField(max_length=122)
  email=models.CharField(max_length=122)
  password=models.CharField(max_length=122)
 
class Test(models.Model):
  image1=models.ImageField(null=True,blank=True,upload_to="images/")
  sub2=models.CharField(max_length=2)
  # bldg=models.CharField(max_length=)

