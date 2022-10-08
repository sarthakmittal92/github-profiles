from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django import forms
from django.contrib.auth.models import User
from dd2app.models import Profile, Repository
from django.core.validators import RegexValidator
from django.utils import timezone
import requests
import datetime

updateError = ''
loggedUser = ''
fullName = ''
username = ''
allowed = RegexValidator(r'^[0-9a-zA-Z@\+\-\._]*$', 'Only alphanumeric and @/+/-/./_ are allowed.')

class UserCreateForm(UserCreationForm):
	first_name = forms.CharField(max_length=100,required=True,validators=[allowed])
	last_name = forms.CharField(max_length=100, required=False,validators=[allowed])
	
	class Meta(UserCreationForm.Meta):
		model = User	
		fields = ('username','password1','password2','first_name','last_name')

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
			global loggedUser, fullName
			loggedUser = str(self.cleaned_data['username'])
			fullName = str(self.cleaned_data['first_name']) + ' ' + str(self.cleaned_data['last_name'])
			FetchAndStore(loggedUser,fullName)
		return user

class SignUpView(generic.CreateView):
	form_class = UserCreateForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'

def FetchAndStore (username, fullName):
	response1 = requests.get('https://api.github.com/users/'+ username)
	string = str(timezone.now())[0:19]
	date = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
	date = date.strftime('%b %d, %Y %I:%M %p')
	response2 = requests.get('https://api.github.com/users/'+ username + '/repos')
	if 'message' not in response1.json() and 'message' not in response2.json():
		saveProfile = Profile(login=username,followers=response1.json()['followers'],updated_at=date,name=fullName)
		saveProfile.save()
		for repo in response2.json():
			repoName = repo['name']
			repoStars = repo['stargazers_count']
			saveRepo = Repository(name=repoName,stars=repoStars,profile=saveProfile)
			saveRepo.save()

def Updater (username, fullName):
	global updateError
	response1 = requests.get('https://api.github.com/users/'+ username)
	string = str(timezone.now())[0:19]
	date = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
	date = date.strftime('%b %d, %Y %I:%M %p')
	response2 = requests.get('https://api.github.com/users/'+ username + '/repos')
	if 'message' not in response1.json() and 'message' not in response2.json():
		updateError = ''
		userProfile = Profile.objects.filter(login=username)
		Repository.objects.filter(profile=userProfile[0]).all().delete()
		Profile.objects.filter(login=username).all().delete()
		saveProfile = Profile(login=username,followers=response1.json()['followers'],updated_at=date,name=fullName)
		saveProfile.save()
		for repo in response2.json():
			repoName = repo['name']
			repoStars = repo['stargazers_count']
			saveRepo = Repository(name=repoName,stars=repoStars,profile=saveProfile)
			saveRepo.save()
	else:
		updateError = 'Could not fetch data, try again later'

def ProfileList (request):
	profileList = Profile.objects.all()
	return render(request,'../templates/registration/explore.html',{'profiles': profileList})#response.json())

def ProfileData (request, string):
	global updateError
	username = string
	userProfile = Profile.objects.filter(login=username)[0]
	profileData = Repository.objects.filter(profile=userProfile).order_by('-stars')
	return render(request,'../templates/registration/profile.html',{'profile':userProfile,'repos': profileData, 'error': updateError})

def UpdateNow (request, string):
	username = string
	userProfile = Profile.objects.filter(login=username)
	name = userProfile[0].name
	Updater (username,name)
	return redirect('/profile/' + username)