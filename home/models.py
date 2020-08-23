from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image


class Videoblog_video(models.Model):
    videolink = models.CharField(max_length=300, blank=True, default="https://www.youtube.com/embed/JrO46CdJd9ns")
    tag = models.CharField(max_length=300, blank=True, default="")
    title = models.CharField(max_length=300, blank=True, default="")
    description = models.TextField(max_length=300, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title + ' on ' + self.tag


class Twelve_rashi(models.Model):
    maish = models.TextField(max_length=913, blank=True)
    vrish = models.TextField(max_length=913, blank=True)
    mithun = models.TextField(max_length=913, blank=True)
    kark = models.TextField(max_length=913, blank=True)
    singh = models.TextField(max_length=913, blank=True)
    kanya = models.TextField(max_length=913, blank=True)
    tula = models.TextField(max_length=913, blank=True)
    vrishchik = models.TextField(max_length=913, blank=True)
    dhanu = models.TextField(max_length=913, blank=True)
    makar = models.TextField(max_length=913, blank=True)
    kumbh = models.TextField(max_length=913, blank=True)
    meen = models.TextField(max_length=913, blank=True)

    def __str__(self):
        return '12 rashi updates.'




class AnswerQuestion(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=213, blank=True, default='')
    dob = models.CharField(max_length=213, blank=True, default='')
    number = models.CharField(max_length=213, blank=True, default='')
    status = models.CharField(max_length=20, blank=False)
    reason = models.TextField(max_length=513, default='', blank=True)
    kundali_answer = models.TextField(max_length=500, default='', blank=True)
    user = models.CharField(max_length=50, blank=True)
    kundaliphoto = models.ImageField(upload_to="kundali_photos", default=None, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name + ", Reason: ( " + self.reason[:40] + '... )'

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
    GENDER_CF = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Custom', 'Custom')
    ]

    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=213 , blank=True, default="")

    username = models.CharField(max_length=60, blank=True, default="")
    profile_photo = models.ImageField(upload_to='profile',  default='profile/default.png')

    dob = models.CharField(max_length=213, blank=True, default="22-02-222222 22:02", null=True)

    # dob = models.DateTimeField(blank=True, null=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CF, blank=True)
    number = models.CharField(max_length=213, default="", blank=True)
    email = models.CharField(max_length=213, blank=True, default="")
    bio = models.TextField(max_length=513, blank=True, default="")
    timestamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.fullname + ' as ' + self.username

    def save(self):
        super().save()
        size_for_thumb = (300, 300)
        pic_for_thumb = Image.open(self.profile_photo.path)
        pic_for_thumb.thumbnail(size_for_thumb)
        pic_for_thumb.save(self.profile_photo.path)


class Newsletter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.CharField(max_length=213, null=True, default="", blank=True)
    name = models.CharField(max_length=213, null=True, default="", blank=True)
    sno = models.AutoField(primary_key=True)

    def __str__(self):
        return self.email

