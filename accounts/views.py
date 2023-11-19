from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
#import redirect
from django.shortcuts import redirect
#import login_required
from django.contrib.auth.decorators import login_required
from .models import Profile , STATE_CHOICES , COUNTRY_CHOICES
from product.models import UserImage , ProductDesign

# Create your views here.
def log_in(request):
    if request.method=="POST":
        #get username , password 
        username = request.POST['username']
        password = request.POST['password']
        #check if user exists
        user = authenticate(username=username, password=password)
        if user is not None:
            #login
            login(request, user)
            #redirect to home page
            return redirect("home:home")
        else:
            #message
            messages.error(request, 'Invalid username or password')
            #redirect to login page
            return redirect("accounts:login")

    return render(request, 'login.html', {})



def log_out(request):
    #logout
    logout(request)
    #redirect to home page
    return redirect("home:home")
    



def register(request):
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
    }
    if request.method=="POST":
        #get first_name , last_name , username , email , phone , password1 , passowrd2 , address , state , Country , State
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email= request.POST['username']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        #check if passwords match
        if password1 != password2:
            #message
            messages.error(request, 'Passwords do not match')
            #redirect to register page
            return redirect("accounts:register")
        
        #check if user exists
        if User.objects.filter(username=username).exists():
            #message
            messages.error(request, 'User already exists')
            #redirect to register page
            return redirect("accounts:register")
        
        #create user and profile
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        profile = Profile.objects.create(user=user, phone=phone, address=address, country=country, state=state)
        
        #login
        login(request, user)
        #redirect to home page
        return redirect("home:home")
    
    
    return render(request, 'register.html', context)



@login_required(login_url="/accounts/login/")
def profile(request):
    #get user
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    if request.method=="POST":
        #get first_name , last_name  , phone , state , Country , image , current_password , new_password 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        state = request.POST['state']
        country = request.POST['country']
        print(country)
        image = request.FILES.get('image',False)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        postal_code=request.POST['postal_code']
        #check if passwords match
        if password1 != password2:
            #message
            messages.error(request, 'Passwords do not match')
            #redirect to profile page
            return redirect("accounts:profile")
        
        #update user and profile for exist data and new data if not exist
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        #if myprofile not exist create it
        if not myprofile:
            myprofile = Profile.objects.create(user=user, phone=phone, country=country, state=state, image=image, postal_code=postal_code)
        else:
            myprofile.phone=phone
            myprofile.state=state
            myprofile.country=country
            myprofile.postal_code=postal_code
            if image:
                myprofile.image=image
            if password1:
                user.set_password(password1)
            myprofile.save()
        user.save()
        #message
        messages.success(request, 'Profile updated successfully')
        #redirect to profile page
        return redirect("accounts:profile")
    
    
        
    return render (request,'profile-info.html',context)

@login_required(login_url="/accounts/login/")
def my_orders(request):
    #get user
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    return render(request,'my-orders.html',context)


@login_required(login_url="/accounts/login/")
def my_images(request):
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    #get user images
    user_images=UserImage.objects.filter(user=user)    
    
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
        'user_images':user_images,
    }
    
    return render(request,'my-Images.html',context)


@login_required(login_url="/accounts/login/")
def my_designs(request):
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    #get user designs
    user_designs=ProductDesign.objects.filter(user=user)    
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
        'user_designs':user_designs,
    }
    
    return render(request,'my-Designs.html',context)


@login_required(login_url="/accounts/login/")
def wishlist(request):
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    return render(request,'wishlist.html',context)


@login_required(login_url="/accounts/login/")
def addresses(request):
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    return render(request,'addresses.html',context)


@login_required(login_url="/accounts/login/")
def payment_methods(request):
    user=request.user
    try:
        # Get the user's profile
        myprofile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        myprofile = None     
    #get state , country if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    return render(request,'payment-methods.html',context)




def forgot_password(request):
    return render(request, 'forgetpassword.html', {})



def reset_password(request):
    return render(request, 'resetePassword.html', {})