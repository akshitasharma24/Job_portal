from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class stuUser(models.Model):
    username = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)         

    def __str__(self):
        return self.username


class stuComp(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username  

class Job(models.Model):
    # Company Info
    company = models.ForeignKey(stuComp, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=100)
    industry_type = models.CharField(max_length=50)
    headquarters = models.CharField(max_length=100)
    established_year = models.IntegerField()
    about_company = models.TextField()

    # Contact Info
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    company_address = models.TextField(null=True,blank=True)

    # Job Info
    job_title = models.CharField(max_length=100)
    job_location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50)
    salary_range = models.CharField(max_length=50)
    experience_required = models.CharField(max_length=50)
    skills_required = models.CharField(max_length=255)
    job_description = models.TextField()

    def __str__(self):
        return self.job_title





class UserProfile(models.Model):
    user=models.OneToOneField(stuUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tenth = models.FloatField()
    twelfth = models.FloatField()
    ug = models.FloatField()
    pg = models.FloatField(null=True, blank=True)
    
    employment_type = models.CharField(max_length=20, choices=[
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract')
    ])
    
    preferred_location = models.CharField(max_length=100)
    preferred_role = models.CharField(max_length=100)
    
    years_exp = models.CharField(max_length=10, choices=[
        ('0-1', '0-1 Years'),
        ('1-3', '1-3 Years'),
        ('3-5', '3-5 Years'),
        ('5+', '5+ Years')
    ])
    
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    preferred_shift = models.CharField(max_length=10, choices=[
        ('day', 'Day Shift'),
        ('night', 'Night Shift'),
        ('flexible', 'Flexible')
    ])
    
    language = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    user = models.ForeignKey(stuUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')])
    
    def __str__(self):
        return f"{self.user.username} - {self.job.job_title}"



class AppliedJob(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)