from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image



class AnswerQuestions(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=213, blank=True, default='')
    dob = models.CharField(max_length=213, blank=True, default='')
    number = models.CharField(max_length=213, blank=True, default='')
    status = models.CharField(max_length=20, blank=False)
    reason = models.TextField(max_length=513, default='', blank=True)
    kundali_answer = models.TextField(max_length=500, default='', blank=True)
    user = models.CharField(max_length=50, blank=True)
    kundaliphoto = models.ImageField(upload_to="profile", default='profile/default.png')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name + self.reason[:20] + '...'

# Create your models here.
class ContactUser(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=213)
    email = models.CharField(max_length=213)
    subject = models.CharField(max_length=213)
    matter = models.CharField(max_length=513)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.email




# Create your models here.
class SigningUser(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=213, null=True, blank=True, default="")
    email = models.CharField(max_length=213, null=True, blank=True, default="")
    passw = models.CharField(max_length=213, null=True, blank=True, default="")
    username = models.CharField(max_length=213, null=True, blank=True, default="")
    gender = models.CharField(max_length=10, null=True, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.fullname + ' as ' + self.username


class Profile(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=213, null=True, blank=True, default="")
    username = models.CharField(max_length=60, null=True, blank=True, default="")
    photo = models.ImageField(upload_to="profile", default='profile/default.png')

    occupation = models.CharField(max_length=213, null=True, blank=True, default="")
    dob = models.CharField(max_length=213, null=True, blank=True, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    marrystatus = models.CharField(max_length=30, blank=True, default="", null=True)
    address = models.CharField(max_length=213, null=True, default="", blank=True)
    number = models.CharField(max_length=213, default="", blank=True, null=True)
    email = models.CharField(max_length=213, blank=True, default="", null=True)
    languages = models.CharField(max_length=213, blank=True, default="English", null=True)
    bio = models.TextField(max_length=513, blank=True, default="", null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.fullname + ' as ' + self.username

    def save(self):
        super().save()
        size_for_thumb = (500, 550)
        pic_for_thumb = Image.open(self.photo.path)
        pic_for_thumb.thumbnail(size_for_thumb)
        pic_for_thumb.save(self.photo.path)


class Newsletter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.CharField(max_length=213, null=True, default="", blank=True)
    name = models.CharField(max_length=213, null=True, default="", blank=True)
    sno = models.AutoField(primary_key=True)

    def __str__(self):
        return self.email

