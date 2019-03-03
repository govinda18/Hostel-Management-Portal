# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_ref
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
import datetime

host_location = 'http://127.0.0.1:8000/'


# Create your views here.
def checkadmin(request):
	isadmin = False
	if(request.user.is_authenticated):
		try:
			hostelprofile = HostelProfile.objects.get(user=request.user)
			isadmin = True
		except:
			isadmin = False
	return isadmin

def Home(request):
	isadmin = checkadmin(request)
	hostel_list = Hostel.objects.all()
	notifications = Notifcation.objects.order_by('-time_stamp')
	return render(request, 'student/home_page.html',{
		"hostels" : hostel_list,
		"notifications" : notifications,
		"isadmin" : isadmin,
		})

def Hostel_View(request,pk):
	isadmin = checkadmin(request)
	hostel = get_object_or_404(Hostel,pk=pk)
	notification = Notifcation.objects.filter(hostel=hostel).order_by('-time_stamp')
	staff = Staff.objects.filter(hostel = hostel)
	return render(request, 'student/hostel.html',{
		"hostel" : hostel,
		"isadmin" : isadmin,
		"notifications" : notification,
		"staff" : staff,
		})

def HostelLoginView(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method=='POST':
		try:
			user = authenticate(username=str(request.POST['form-username']),password=request.POST['form-password'])
			hostel = HostelProfile.objects.get(user=User.objects.get(username=request.POST['form-username']))
			login_ref(request,user)
		except Exception as e:
			messages.error(request,e)
			return render(request,'student/hostel_login_form.html')
		
		return redirect('/hostel/'+str(hostel.id)+'/')	
	return render(request,'student/hostel_login_form.html')

def LogoutView(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login')
	isadmin = checkadmin(request)
	logout(request)
	messages.success(request,"Successfully logged out.")
	if isadmin:
		return redirect('/hostel/login')
	else:
		return redirect('/student/login')
	return redirect('/')

def AddNotification(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/hostel/login')
	isadmin = checkadmin(request)
	if not isadmin:
		return redirect('/')
	hostelprofile = HostelProfile.objects.get(user=request.user)
	if request.method == 'POST':
		notification = Notifcation()
		notification.hostel = hostelprofile.hostel
		notification.link = request.POST['form-link']
		notification.message = request.POST['form-message']
		notification.save()
		return redirect('/hostel/' + str(hostelprofile.hostel.id) + '/')	
	return render(request, 'student/notifications_form.html',{
		"isadmin" : isadmin,
		"hostel" : hostelprofile.hostel,
		})

def DeleteNotification(request,pk):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/hostel/login')
	isadmin = checkadmin(request)
	if not isadmin:
		return redirect('/')
	try:
		notification = Notifcation.objects.get(pk=pk)
	except:
		messages.error(request, "Error Deleting Notification.")
		return redirect("/")
	hostelprofile = HostelProfile.objects.get(user=request.user)
	if notification.hostel != hostelprofile.hostel:
		messages.error(request, "You are not authorized to delete this notification.")
		return redirect("/")
	notification.delete()
	return redirect('/hostel/' + str(hostelprofile.id) + '/')


def UpdateHostel(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/hostel/login')
	isadmin = checkadmin(request)
	if not isadmin:
		return redirect('/')
	hostelprofile = HostelProfile.objects.get(user=request.user)
	hostel=hostelprofile.hostel
	if request.method == 'POST':
		hostel.number_of_students = request.POST['form-numberofstudents']
		hostel.mess1_maharaj_name = request.POST['form-mess1maharaj']
		hostel.mess2_maharaj_name = request.POST['form-mess2maharaj']
		hostel.mess3_maharaj_name = request.POST['form-mess3maharaj']
		hostel.mess_bill_link = request.POST['form-messbill']
		hostel.student_list = request.POST['form-studentlist']
		hostel.canteen_menu = request.POST['form-menu']
		hostel.HEC = request.POST['form-hec']
		hostel.wardens = request.POST['form-wardens']
		hostel.care_takers = request.POST['form-caretakers']
		hostel.maintainance_workers = request.POST['form-workers']
		hostel.save()
		return redirect('/hostel/' + str(hostelprofile.hostel.id) + '/')
	return render(request, 'student/hostel_update_form.html',{
		"isadmin" : isadmin,
		"hostel" : hostel,
		})	

def StudentLogin(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		mail=request.POST['form-email'].strip()
		mail=mail.lower()
		user = authenticate(username=mail, password=request.POST['form-password'])
		if user is None:
			try:
				user = User.objects.get(username=request.POST['form-email'])
			except:
				user = None
			if(user is None):
				messages.error(request, "This Email Is Not Registered.")
				return redirect("/student/login")
			messages.error(request, "Invalid Credentials.")
			return redirect("/student/login")
		try:
			profile = Profile.objects.get(user_ref = user)
		except:
			messages.error(request, "Invalid Credentials.")
			return redirect("/student/login")
		if not profile.verified:
			messages.error(request, "Email Id not verified. <a href='/register/resend_validation?uid=%s'>Resend Email?</a>" % (profile.id),extra_tags='safe')
			return redirect("/student/login")		
		login_ref(request,user)
		return redirect('/')
	return render(request, 'student/login_form.html')

def StudentProfile(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue.")
		return redirect('/student/login')
	isadmin = checkadmin(request)
	if isadmin:
		return redirect('/')
	try:
		profile = Profile.objects.get(user_ref = request.user)
	except:
		return redirect('/')
	if request.method == 'POST':
		if 'hostel' in request.POST:
			try:
				hostel = Hostel.objects.get(pk=request.POST['hostel'])
			except:
				messages.error(request, "Invalid Hostel Selected.")
				return redirect('/student/profile/')
			profile.hostel = hostel
		if 'room' in request.POST:
			try:
				roomno = int(request.POST['room'])
			except:
				messages.error(request, "Please enter a valid room number.")
				return redirect('/student/profile/')
			profile.room_no = request.POST['room']
		if 'year' in request.POST:
			try:
				year = int(request.POST['year'])
			except:
				messages.error(request, "Please enter a valid year of study.")
				return redirect('/student/profile/')
			profile.year = request.POST['year']
		profile.save()
	hostels = Hostel.objects.all().order_by('hostel_name')
	branches = Branch.objects.all().order_by('name')
	return render(request, 'student/profile.html',{
		"profile" : profile,
		"hostels" : hostels,
		"isadmin" : isadmin,
		"branches" : branches,
		})

def ChangePassword(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	if isadmin:
		return redirect('/')
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('/student/profile/')
		else:
			messages.error(request, form.errors)
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'student/change_password.html', {
		'form': form,
		"isadmin" : isadmin,
	})

def ForgotPassword(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		if 'form-email' not in request.POST:
			messages.error(request, "Incomplete Information.")
			return redirect('/student/forgotpass/')
		try:
			mail = request.POST['form-email'].strip()
			mail = mail.lower()
			profile = Profile.objects.get(emailid=mail)
		except:
			messages.error(request, "Email id not registered.")
			return redirect('/student/register/')
		pswd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		matter = 'Your password has been reset.\n'
		matter += 'You can change your password later under Profile tab.\n\n'
		matter += 'Password - ' + pswd
		matter += '\n\n\n'
		matter += 'Regards\n Hostel Web Committee'
		user = User.objects.get(pk = profile.user_ref.id)
		user.set_password(pswd)
		user.save()
		send_mail(
				'Reset Password for Hostel Portal',
				matter,
				settings.DEFAULT_FROM_EMAIL,
				[request.POST['form-email']],
				fail_silently=False,
			)
		messages.success(request, "Password has been reset successfully. Please check your mail.")
		return redirect('/student/login/')
	return render(request, 'student/forgot_password.html')

def StudentRegister(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		print(request.POST)
		required = ['year','form-first-name','form-last-name','form-email','form-rollno','form-branch','form-hostel','form-pass','form-passagain']
		for item in required:
			if item not in request.POST:
				messages.error(request, "Incomplete Information.")
				return redirect("/student/register")
		mail=request.POST['form-email'].strip()
		mail=mail.lower()
		try:
			player = Profile.objects.get(emailid = mail)
		except:
			player = None
		print(player)
		if (player is not None):
			messages.error(request, "Email ID has already been registered.")
			return redirect("/student/login/")
		if '@itbhu.ac.in' not in mail:
			messages.error(request,"Email address is not valid. Please use mail id with @itbhu.ac.in only.")
			return redirect("/student/register")
		if request.POST['form-pass'] != request.POST['form-passagain']:
			messages.error(request, "Paasword do not match.")
			return redirect("/student/register")
		pswd = request.POST['form-pass']
		user = User.objects.create_user(username=mail, password=pswd, email=mail)
		user.save()
		cur_hostel = Hostel.objects.get(pk=request.POST['form-hostel'])
		cur_dept = Branch.objects.get(pk=request.POST['form-branch'])
		profile = Profile(user_ref=user, first_name=request.POST['form-first-name'], last_name=request.POST['form-last-name'], branch=cur_dept, emailid=mail, hostel=cur_hostel, rollno=request.POST['form-rollno'],year=request.POST['year'])
		profile.save()
		global host_location
		activation = Activation(profile_ref = profile)
		activation_code = activation.getActivationCode(profile.emailid)
		activation.activation_code = activation_code
		activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
		activation.save()
		send_mail(
				'Activation Link for Hostel Management Portal',
				'Hi, %s!\n\nYour account was successfully created on hostel management portal of IIT (BHU), Varanasi.\n\nPlease verify your Email ID by clicking this link:\n %sstudent/checkmail/?ac=%s \n\nRegards,\nTeam Hostel Web Committee'%(profile.first_name,host_location,activation_code),
				settings.DEFAULT_FROM_EMAIL,
				[profile.emailid],
				fail_silently=False,
			)
		messages.success(request,"Account successfully created. Please check your mail box for verification link. Please verify your mail.")
		return redirect('/student/login')

	hostels = Hostel.objects.all().order_by('hostel_name')
	branches = Branch.objects.all().order_by('name')
	return render(request,'student/register_form.html',{
		'hostels':hostels,
		"branches" : branches,
		})

def ResendMail(request):
	if(request.user.is_authenticated):
		return redirect('/', permanent=True)
	if('err' in request.GET):
		messages.error(request, "Unknown error occured.")
		return redirect('/student/login/')
	if('uid' not in request.GET):
		messages.error(request, "Unknown error occured.")
		return redirect('/student/login/')
	else:
		try:
			profile = Profile.objects.get(pk = request.GET['uid'])
		except:
			messages.error(request, "Unknown error occured.")
			return redirect('/student/login/')
		if profile is not None:
			if profile.verified:
				messages.success(request, "Email id is already verified.")
				return redirect('/student/login/')
			global host_location
			try:
				activation = Activation.objects.get(profile_ref = profile)
				activation_code = activation.activation_code
				activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
				activation.save()
			except:
				activation = Activation(profile_ref = profile)
				activation_code = activation.getActivationCode(profile.email)
				activation.activation_code = activation_code
				activation.expiry = datetime.datetime.today().date() + datetime.timedelta(2)
				activation.save()
			send_mail(
			'Activation Link for Hostel Management Portal',
			'Hi, %s!\n\nYour account was successfully created on hostel management portal of IIT (BHU), Varanasi.\n\nPlease verify your Email ID by clicking this link:\n %sstudent/checkmail/?ac=%s \n\nRegards,\nTeam Hostel Web Committee'%(profile.first_name,host_location,activation_code),
			settings.DEFAULT_FROM_EMAIL,
			[profile.emailid],
			fail_silently=False,
			)
			messages.success(request, "Activation mail has been sent again. Please verify your Email ID.")
			return redirect("/student/login/")
	return redirect('/student/login/')

def CheckMailView(request):
	if(request.method == "GET" and 'ac' in request.GET):
		try:
			activation = Activation.objects.get(activation_code = request.GET['ac'])
		except:
			activation = None
			messages.error(request, "Email ID not registered.")
			return redirect("/student/register/")
		if activation.profile_ref.verified:
			messages.error(request, "Email ID already verified.")
			return redirect("/student/login/")
		if(datetime.datetime.today().date() > activation.expiry):
			messages.error(request, "Verification code expired. <a href='/register/resend_validation?uid=%s'>Resend Email?</a>" % (activation.profile_ref.id),extra_tags='safe')
			return redirect("student/login/")
		activation.profile_ref.verified = True
		activation.profile_ref.save()
		profile = activation.profile_ref
		messages.success(request, "Email ID successfully verified. Log in to continue.")
		return redirect("/student/login/")
	messages.error(request, "Unknown error occurred. Please try again.")
	return render(request, '/student/login/')


def AddGrievance(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	if isadmin:
		return redirect('/')
	if request.method == 'POST':
		required = ['form-hostel', 'form-category', 'form-subject', 'form-desc']
		for i in required:
			if i not in request.POST:
				messages.error(request, "Incomplete Information.")
				return redirect('/student/addgrievance/')
		grievance = Grievance()
		grievance.user = request.user
		profile = Profile.objects.get(user_ref = grievance.user)		
		try:
			grievance.hostel = Hostel.objects.get(pk=request.POST['form-hostel'])
		except:
			messages.error(request, "Invalid Hostel")
			return redirect('/student/addgrievance/')
		try:
			grievance.category = GrievanceCategory.objects.get(pk=request.POST['form-category'])
		except:
			messages.error(request, "Invalid Category")
			return redirect('/student/addgrievance/')
		grievance.subject = request.POST['form-subject']
		grievance.description = request.POST['form-desc']
		grievance.save()
		matter = 'Hi ' + profile.first_name + ',\n\n'
		matter += 'Your grievance was successfully registered with us.'
		matter += ' You can track the status of your grievance using the following link - \n'
		matter += host_location + 'hostel/grievance/' + str(grievance.id) + '/'
		matter += '\n\n'
		matter += 'Thanks\n'
		matter += 'Regards\n'
		matter += 'Team Hostel Web Committee' 
		send_mail(
		'Grievance Posted Successfully',
		matter,
		settings.DEFAULT_FROM_EMAIL,
		[profile.emailid],
		fail_silently=False,
		)
		return redirect('/student/grievances/')


	hostels = Hostel.objects.all().order_by('-hostel_name')
	categories = GrievanceCategory.objects.all().order_by('name')
	return render(request, 'student/grievance_form.html',{
		"hostels" : hostels,
		"categories" : categories,
		"isadmin" : isadmin,
		})

def ViewStudentGrievances(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	if isadmin:
		return redirect('/')
	grievances = Grievance.objects.all().order_by('-date')
	paginator = Paginator(grievances, 25)
	page = request.GET.get('page')
	if not page:
		page = 1
	grievancelist = paginator.page(page) 
	return render(request, 'student/grievances.html', {
		"grievances" : grievancelist,
		"isadmin" : isadmin,
		})

def ViewHostelGrievances(request):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	if not isadmin:
		return redirect('/student/viewgrievances')
	hostelprofile = HostelProfile.objects.get(user=request.user)
	grievances = Grievance.objects.filter(hostel = hostelprofile.hostel).order_by('-date')
	return render(request, 'student/grievances.html', {
		"grievances" : grievances,
		"isadmin" : isadmin,
		})


def ViewGrievanceDetail(request,pk):
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	try:
		grievance = Grievance.objects.get(pk=pk)
		userprofile = Profile.objects.get(user_ref=grievance.user)
	except:
		messages.error(request, 'No such grievance found.')
		return redirect('/student/grievances')
	if not isadmin:
		return render(request, 'student/grievance_detail.html', context = {
			"grievance" : grievance,
			"profile" : userprofile,
			"isadmin" : isadmin
			})
	if request.method == 'POST':
		flag_for_mail_send = False
		if 'expected_date' in request.POST:
			if request.POST['expected_date']: 
				if grievance.expected_date != request.POST['expected_date']:
					flag_for_mail_send = True
					grievance.expected_date = request.POST['expected_date']
		if 'status' in request.POST:
			if grievance.status != request.POST['status']:
				flag_for_mail_send = True 	
				grievance.status = request.POST['status']
		if 'comment' in request.POST:
			if grievance.comment != request.POST['comment']:
				flag_for_mail_send = True
				grievance.comment = request.POST['comment']
		if flag_for_mail_send:
			matter = 'Hi ' + userprofile.first_name + ',\n\n'
			matter += 'Your grievance status was recently updated.'
			matter += ' You can track the status of your grievance using the following link - \n'
			matter += host_location + 'hostel/grievance/' + str(grievance.id) + '/'
			matter += '\n\n'
			matter += 'Thanks\n'
			matter += 'Regards\n'
			matter += 'Team Hostel Web Committee' 
			send_mail(
			'Grievance Status Updated',
			matter,
			settings.DEFAULT_FROM_EMAIL,
			[userprofile.emailid],
			fail_silently=False,
			)
		grievance.save()
		messages.success(request, "Updated Successfully.")
		return redirect('/hostel/grievances/')
	return render(request, 'student/updategrievance.html',{
		"grievance" : grievance,
		"isadmin" : isadmin,
		"profile" : userprofile,
		})


lock = False

def AllotRoom(request):
	global lock
	if not request.user.is_authenticated:
		messages.error(request, "Please login to continue")
		return redirect('/student/login/')
	isadmin = checkadmin(request)
	if isadmin:
		return redirect('/')
	profile = Profile.objects.get(user_ref = request.user)
	hostelscheme = HostelAllotment.objects.get(branch = profile.branch, year=profile.year)
	rooms = []
	try:
		roominfo = Roominfo.objects.get(member1 = profile)
		messages.success(request, "Room no. " + str(roominfo.room_no) + " in hostel " + roominfo.scheme.hostel.hostel_name + " has already been allocated to you.")
		return redirect('/student/profile')
	except:
		pass
	try:
		roominfo = Roominfo.objects.get(member2 = profile)
		messages.success(request, "Room no. " + str(roominfo.room_no) + " in hostel " + roominfo.scheme.hostel.hostel_name + " has already been allocated to you.")
		return redirect('/student/profile')
	except:
		pass
	try:
		roominfo = Roominfo.objects.get(member3 = profile)
		messages.success(request, "Room no. " + str(roominfo.room_no) + " in hostel " + roominfo.scheme.hostel.hostel_name + " has already been allocated to you.")
		return redirect('/student/profile')
	except:
		pass
	if request.method == 'POST':
		while lock:
			continue
		lock=True
		room_selected = request.POST['select']
		roominfo = Roominfo.objects.get(pk=room_selected)
		if roominfo.is_filled:
			messages.error(request, 'Room is already occupied.')
			return redirect('/student/allotroom/')
		if roominfo.member1 is None:
			roominfo.member1 = profile
			roominfo.save()
			messages.success(request, "Room alloted successfully.")
		elif roominfo.member2 is None:
			roominfo.member2 = profile
			roominfo.save()
			messages.success(request, "Room alloted successfully.")
		elif roominfo.member3 is None:
			roominfo.member2 = profile
			roominfo.save()
			messages.success(request, "Room alloted successfully.")
		roominfo.count += 1
		if roominfo.count >= roominfo.scheme.per_room:
			print("value")
			roominfo.is_filled = True
		lock = False
		return redirect('/student/profile')
	for i in range(hostelscheme.start_room,hostelscheme.end_room+1):
		rooms.append(Roominfo.objects.get(room_no=i,scheme=hostelscheme)) 
	return render(request, 'student/roomallocation.html',{
		"rooms" : rooms,
		"isadmin" : isadmin,
		})
