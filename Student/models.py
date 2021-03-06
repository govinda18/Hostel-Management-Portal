# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.crypto import get_random_string
import hashlib
# Create your models here.


class Hostel(models.Model):
	hostel_name = models.CharField(max_length=1000)
	location = models.CharField(max_length=1000)
	rooms = models.PositiveIntegerField(default=0)
	hostel_image1 = models.ImageField(upload_to='hostel_images')
	hostel_image2 = models.ImageField(upload_to='hostel_images')
	hostel_image3 = models.ImageField(upload_to='hostel_images')
	flag_image = models.ImageField(upload_to='hostel_images',null=True)
	number_of_students = models.PositiveIntegerField(default=0)
	mess1_maharaj_name = models.CharField(max_length=100,null=True)
	mess2_maharaj_name = models.CharField(max_length=100,null=True)
	mess3_maharaj_name = models.CharField(max_length=100,null=True)
	mess_bill_link = models.CharField(max_length=500,null=True)
	student_list = models.CharField(max_length=500,null=True)
	canteen_menu = models.CharField(max_length=500,null=True)
	HEC = models.CharField(max_length=500,null=True)
	wardens = models.CharField(max_length=500,null=True)
	care_takers = models.CharField(max_length=500,null=True)
	maintainance_workers = models.CharField(max_length=500,null=True)
	duties_of_hec = models.CharField(max_length=500,null=True)

	def __str__(self):
		return self.hostel_name

class Notifcation(models.Model):
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True)
	link = models.CharField(max_length=2000, null=True, blank=True)
	message = models.TextField()
	time_stamp = models.DateTimeField(default=datetime.now())

	def __str__(self):
		return self.message

class HostelProfile(models.Model):
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.hostel.hostel_name

class Branch(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=100, default='B.tech')

	def __str__(self):
		return self.name

class Profile(models.Model):
    rollno=models.PositiveIntegerField(default=0)
    user_ref=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE,null=True)
    room_no = models.PositiveIntegerField(default=-1)
    year = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    emailid = models.EmailField()
    verified= models.BooleanField(default=False)
    def __str__(self):
        return self.first_name+" "+self.last_name

class GrievanceCategory(models.Model):
	name = models.CharField(max_length=100)
	authority = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Grievance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(GrievanceCategory, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField('Subject', max_length=200, blank=True)
    date  = models.DateTimeField(null=False,blank=True,default=datetime.now())
    description = models.CharField('Description', max_length=1000, blank=True)
    expected_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=200,default='Pending')
    comment = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
    	return self.subject + ' - ' + str(self.date)

class HostelAllotment(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	year = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
	hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
	start_room = models.PositiveIntegerField(default=1)
	end_room = models.PositiveIntegerField(default=1)
	per_room = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(3)])

	def __str__(self):
		return str(self.branch) + ' - ' + str(self.year) + ' year'

class Roominfo(models.Model):
    room_no = models.IntegerField(blank=False,null=False)
    member1 = models.ForeignKey(Profile,blank=True,null=True,related_name='mem1', on_delete=models.SET_NULL)
    member2 = models.ForeignKey(Profile,blank=True,null=True,related_name='mem2', on_delete=models.SET_NULL)
    member3 = models.ForeignKey(Profile,blank=True,null=True,related_name='mem3', on_delete=models.SET_NULL)
    scheme = models.ForeignKey(HostelAllotment, on_delete=models.CASCADE,null=True)
    is_filled = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=0)
    in_queue = models.BooleanField(default=False)
    timestamp = models.DateTimeField(blank=True,null=True)

    def __str__(self):
    	return "Room no. " + str(self.room_no) + " - " + str(self.scheme.hostel)

class Activation(models.Model):
    profile_ref = models.OneToOneField(Profile)
    activation_code = models.CharField(max_length = 50)
    expiry = models.DateField(auto_now_add=False)
    def getActivationCode(self, username):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(20, chars)
        return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()

class Staff(models.Model):
	name = models.CharField(max_length = 150)
	post = models.CharField(max_length = 150)
	contact_no = models.PositiveIntegerField(default = 0)
	emailid = models.CharField(max_length = 150)
	profilepic = models.ImageField(upload_to = 'staff_images',null = True)
	hostel = models.ForeignKey(Hostel, on_delete = models.CASCADE)

	def __str__(self):
		return self.name + ' - ' + self.post + ' - ' + str(self.hostel)

class LostFound(models.Model):
	user = models.ForeignKey(Profile, on_delete = models.CASCADE)
	label = models.BooleanField(default = False) # False for Lost
	date = models.DateField(null=False,blank=True,default=datetime.now())
	subject = models.CharField(max_length = 100)
	item_info = models.TextField()
	location_info = models.TextField()
	item_image1 = models.ImageField(upload_to = 'lostfound_images', null = True)
	item_image2 = models.ImageField(upload_to = 'lostfound_images', null = True)
	item_image3 = models.ImageField(upload_to = 'lostfound_images', null = True)

	def __str__(self):
		return self.subject + ' - ' + ("Found" if self.label else "Lost")

class Contributor(models.Model):
	name = models.CharField(max_length = 150)
	imageurl = models.CharField(max_length = 300)
	rollno = models.PositiveIntegerField(default=0)
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
	email = models.CharField(max_length = 150)
	github = models.CharField(max_length = 150)
	linkedin = models.CharField(max_length = 150)

	def __str__(self):
		return self.name
