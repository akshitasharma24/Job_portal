from .models import stuUser, Job, stuComp, UserProfile, Application, AppliedJob
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session
User=get_user_model()



# Create your views here.
def HomePage(request):
    return render(request, 'home.html')


def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        # Validate input
        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return redirect("LoginPage")

        try:
            user = stuUser.objects.get(username=username)

            #  Password verification (plaintext comparison)
            if check_password(password,user.password):  
                request.session['user_id'] = user.id
                request.session['username'] = user.username 
                request.session['reset_username']=user.username 
                request.session.modified = True  
                messages.success(request, "Login successful!")
             
                return redirect("DashboardPage")  # Redirect to user dashboard
            else:
                messages.error(request, "Invalid password. Please try again!")

        except stuUser.DoesNotExist:
            messages.error(request, "User not found. Please check your username.")

    return render(request,"login1.html")


def PasswordPage(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Username from session (set during forget flow OR directly from login if set)
        username = request.session.get('reset_username') or request.session.get('username')

        if not username:
            messages.error(request, "Session expired. Please login again.")
            return redirect("LoginPage")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "password.html")

        try:
            user = stuUser.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully!")
            return redirect("LoginPage")
        except stuUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("LoginPage")

    return render(request, "password.html")


def RegisterPage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again!")
            return redirect("RegisterPage")

        # Check if username already exists
        if stuUser.objects.filter(username=name).exists():
            messages.error(request, "Username already exists. Please use another one!")
            return redirect("RegisterPage")

        # Check if email already exists
        if stuUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use another one!")
            return redirect("RegisterPage")

        # Create and save user
        user = stuUser.objects.create(
            username=name,
            email=email,
            password=make_password(password)
        )
        request.session['user_id']=user.id
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect("EditProfile")

    return render(request, "register.html")



def DashboardPage(request):
    if 'user_id' not in request.session:
        return redirect("LoginPage")  # Agar user logged in nahi hai toh redirect karo

    user_id = request.session['user_id']
    username = request.session.get('username', 'Guest')


    return render(request, "dashboard.html", {"username": username})

def to_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal('0.00')  # ya None, agar allow karna ho


def EditProfile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('RegisterPage')  

    profile = UserProfile.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        if not profile:
            profile = UserProfile(user_id=user_id)
        profile.name = request.POST.get('name')
        profile.dob = request.POST.get('dob')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.tenth = request.POST.get('tenth')
        profile.twelfth = request.POST.get('twelfth')
        profile.ug = request.POST.get('ug')
        profile.pg = request.POST.get('pg') or None
        profile.employment_type = request.POST.get('employment_type')
        profile.preferred_location = request.POST.get('preferred_location')
        profile.preferred_role = request.POST.get('preferred_role')
        profile.years_exp = request.POST.get('years_exp')
        profile.current_salary = to_decimal(request.POST.get('current_salary'))
        profile.expected_salary = to_decimal(request.POST.get('expected_salary'))
        profile.preferred_shift = request.POST.get('preferred_shift')
        profile.language = request.POST.get('language')

        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']

        profile.save()
        messages.success(request, "Profile saved successfully!")
        return redirect('DashboardPage')

    return render(request, 'editprofile.html', {'profile': profile})
    

def ViewProfile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "User not logged in.")
        return redirect("LoginPage")

    try:
        profile = UserProfile.objects.get(user_id=user_id)

        if request.method == 'POST':
            profile.name = request.POST.get('name')
            profile.dob = request.POST.get('dob')
            profile.email = request.POST.get('email')
            profile.phone = request.POST.get('phone')
            profile.tenth = request.POST.get('tenth')
            profile.twelfth = request.POST.get('twelfth')
            profile.ug = request.POST.get('ug')
            profile.pg = request.POST.get('pg') or None
            profile.employment_type = request.POST.get('employment_type')
            profile.preferred_location = request.POST.get('preferred_location')
            profile.preferred_role = request.POST.get('preferred_role')
            profile.years_exp = request.POST.get('years_exp')
            profile.current_salary = request.POST.get('current_salary')
            profile.expected_salary = request.POST.get('expected_salary')
            profile.preferred_shift = request.POST.get('preferred_shift')
            profile.language = request.POST.get('language')

            if request.FILES.get('resume'):
                profile.resume = request.FILES['resume']
                profile.save()

            
            messages.success(request, "Profile updated successfully!")
            return redirect("ViewProfile")

        return render(request, "viewprofile.html", {"profile": profile})

    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("EditProfile")  

    
def DeleteProfile(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            profile.delete()
            messages.success(request, "Your profile has been deleted successfully.")
        except UserProfile.DoesNotExist:
            messages.warning(request, "No profile found to delete.")
        
        return redirect('EditProfile')  # Redirect to create user profile page
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('LoginPage')


def Complogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return redirect("Complogin")

        # Check if user exists in stuComp
        try:
            company = stuComp.objects.get(username=username)
            # Verify password

            if check_password(password, company.password):
                request.session['company_id'] = company.id  # Save company ID in session
                request.session['comp_reset_username']=company.username
                messages.success(request, "Login successful!")
                return redirect("CompDash")  # Redirect to company dashboard
            else:
                messages.error(request, "Invalid password. Please try again!")
                return redirect("Complogin")

        except stuComp.DoesNotExist:
            messages.error(request, "User not found. Please check your username.")
            return redirect("Complogin")

    return render(request, "complogin.html")





def CompPass(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        username = request.session.get('comp_reset_username')

        if not username:
            messages.error(request, "Session expired. Please enter your username again.")
            return redirect("Complogin")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "comppass.html")

        try:
            company = stuComp.objects.get(username=username)
            company.password = make_password(new_password)
            company.save()
            messages.success(request, "Password updated successfully!")
            return redirect("Complogin")
        except stuComp.DoesNotExist:
            messages.error(request, "Company not found.")
            return redirect("Complogin")

    return render(request, "comppass.html")



def CompReg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again!")
            return redirect("CompReg")

        # Check if username already exists
        if stuComp.objects.filter(username=name).exists():
            messages.error(request, "Username already exists. Please use another one!")
            return redirect("CompReg")

        # Check if email already exists
        if stuComp.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use another one!")
            return redirect("CompReg")

        # Create and save user
        user = stuComp.objects.create(
            username=name,
            email=email,
            password=make_password(password)
        )
        user.save()
        messages.success(request, "Registration successful! Please login.")
        request.session['company_id']=user.id
        return redirect("PostJob")

    return render(request, 'compreg.html')


def CompDash(request):
    # Check if the company is logged in
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect("Complogin")  # Redirect to login if not authenticated

    # Fetch company details
    try:
        company = stuComp.objects.get(id=company_id)
    except stuComp.DoesNotExist:
        return redirect("Complogin")

    # Pass company data to the template
    return render(request, "compdash.html", {"company": company})




def PostJob(request):
    if request.method == "POST":
        company_id=request.session.get('company_id')
        if not company_id:
            messages.error(request,"you must be loged in to post a job")
            return redirect("Complogin")

        try:
            company=stuComp.objects.get(id=company_id)
        except stuComp.DoesNotExist:
            messages.error(request,"Company profile not Found")
            return redirect("Complogin")

        # Get all form data
        company_name = request.POST.get('company_name')
        industry_type = request.POST.get('industry_type')
        headquarters = request.POST.get('headquarters')
        established_year = request.POST.get('established_year')
        about_company = request.POST.get('about_company')

        contact_person = request.POST.get('contact_person')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        company_address = request.POST.get('company_address')

        job_title = request.POST.get('job_title')
        job_location = request.POST.get('job_location')
        employment_type = request.POST.get('employment_type')
        salary_range = request.POST.get('salary_range')
        experience_required = request.POST.get('experience_required')
        skills_required = request.POST.get('skills_required')
        job_description = request.POST.get('job_description')

        # Save to Job model
        try:
            job = Job.objects.create(
                company=company,
                company_name=company_name,
                industry_type=industry_type,
                headquarters=headquarters,
                established_year=established_year,
                about_company=about_company,
                contact_person=contact_person,
                contact_email=contact_email,
                contact_phone=contact_phone,
                company_address=company_address,
                job_title=job_title,
                job_location=job_location,
                employment_type=employment_type,
                salary_range=salary_range,
                experience_required=experience_required,
                skills_required=skills_required,
                job_description=job_description
            )
            job.save()
            messages.success(request, "Job Posted Successfully")
            return redirect("CompDash")
        except Exception as e:
            messages.error(request, f"Error {str(e)}")
            return redirect("PostJob")
    return render(request, 'postjob.html')


def Joblist(request):
    jobs = Job.objects.all()  # Fetch all jobs
    return render(request, 'joblist.html', {'jobs': jobs})

def JobDetails(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    user_id = request.session.get('user_id')
    show_apply_button = False
    profile_missing = False

    if user_id:
        try:
            user = stuUser.objects.get(id=user_id)
            
            # Check if profile exists
            if UserProfile.objects.filter(user=user).exists():
                # Check if already applied
                if not Application.objects.filter(user=user, job=job).exists():
                    show_apply_button = True  # Show apply button only if profile exists and not already applied
            else:
                profile_missing = True  # User logged in but profile not created

        except stuUser.DoesNotExist:
            pass  # Optionally handle invalid session case

    return render(request, 'jobdetails.html', {
        'job': job,
        'show_apply_button': show_apply_button,
        'profile_missing': profile_missing})

def ApplyJob(request, job_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(stuUser, id=user_id)
        job = get_object_or_404(Job, id=job_id)

        # Check if already applied
        if not Application.objects.filter(user=user, job=job).exists():
            Application.objects.create(user=user, job=job, status='Pending')

        # Show thank-you page
        return render(request, 'apply.html', {'job': job})
    else:
        return redirect('LoginPage')



def SearchJob(request):
    results = None  

    if request.method == "POST":
        skills = request.POST.get('skills', '').strip()
        location = request.POST.get('location', '').strip()

        if skills and location:
            results = Job.objects.filter(
                job_title__icontains=skills, 
                job_location__icontains=location
            )
        elif skills:
            results = Job.objects.filter(job_title__icontains=skills)
        elif location:
            results = Job.objects.filter(job_location__icontains=location)

    return render(request, "search.html", {"results":results})


def PostedJobs(request):
    company_id = request.session.get('company_id')
    if not company_id:
        messages.error(request, "Please login as a company.")
        return redirect("Complogin")

    try:
        company = stuComp.objects.get(id=company_id)
    except stuComp.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect("Complogin")

    jobs = Job.objects.filter(company=company)  # not company_id
    return render(request, 'postedjobs.html',{'jobs': jobs})


def DeleteJob(request, job_id):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect("Complogin")

    job = get_object_or_404(Job, id=job_id, company_id=company_id)
    job.delete()
    messages.success(request, "Job deleted successfully!")
    return redirect('PostedJobs')

def UpdateJob(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id)

        # Company info
        job.company_name = request.POST.get('company_name')
        job.industry_type = request.POST.get('industry_type')
        job.headquarters = request.POST.get('headquarters')
        job.established_year = request.POST.get('established_year')
        job.about_company = request.POST.get('about_company')
        job.contact_person = request.POST.get('contact_person')
        job.contact_email = request.POST.get('contact_email')
        job.contact_phone = request.POST.get('contact_phone')
        job.company_address = request.POST.get('company_address')

        # Job info
        job.job_title = request.POST.get('job_title')
        job.job_location = request.POST.get('job_location')
        job.employment_type = request.POST.get('employment_type')
        job.salary_range = request.POST.get('salary_range')
        job.experience_required = request.POST.get('experience_required')
        job.skills_required = request.POST.get('skills_required')
        job.job_description = request.POST.get('job_description')

        job.save()
        messages.success(request, "Job updated successfully.")
    return redirect('PostedJobs')



def MyJobs(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('LoginPage')

    user = get_object_or_404(stuUser, id=user_id)
    applications = Application.objects.filter(user=user).select_related('job')
    return render(request, 'myjobs.html', {'applications': applications})


 
def DeleteAppliedJob(request, application_id):
    user_id = request.session.get('user_id')

    if user_id and request.method == 'POST':
        try:
            user = stuUser.objects.get(id=user_id)
            application = Application.objects.get(id=application_id, user=user)
            application.delete()
        except Application.DoesNotExist:
            pass

    return redirect('MyJobs')


def logout(request):
    # Just remove user_id from session, if you're using custom session auth
    if 'user_id' in request.session:
        del request.session['user_id']
        
    return redirect('HomePage')  # Make sure this name exists in your urls.py


def Applicants(request):
    comp_id = request.session.get('company_id')

    if not comp_id:
        messages.error(request, "Please log in to view applicants.")
        return redirect("Complogin")

    try:
        company = stuComp.objects.get(id=comp_id)
    except stuComp.DoesNotExist:
        messages.error(request, "Company does not exist.")
        return redirect("Complogin")

    jobs = Job.objects.filter(company=company)
    applications = Application.objects.filter(job__in=jobs).select_related('user')

    applicant_profiles = []
    for app in applications:
        profile = UserProfile.objects.filter(user=app.user).first()
        if profile:
            applicant_profiles.append({
                'application': app,
                'profile': profile
            })

    return render(request, 'applicants.html', {'applicant_profiles': applicant_profiles})


def UpdateStatus(request, app_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=app_id)
        application.status = new_status
        application.save()
        return redirect('Applicants')  # Redirect to applicants page


def DeleteApplication(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    application.delete()
    return redirect('Applicants')


def Complogout(request):
    if 'company_id' in request.session:
        del request.session['company_id']
        
    return redirect('HomePage') 

