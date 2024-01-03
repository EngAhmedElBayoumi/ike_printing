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
from product.models import Order
from contact_us.models import ContactList
#import send mail
from django.core.mail import send_mail
#import settings
from django.conf import settings

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
    }
    if request.method=="POST":
        #get first_name , last_name , username , email , phone , password1 , passowrd2 , address , state , city , State
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email= request.POST['username']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        address_line2 = request.POST['address_line2'] 
        if not address_line2:
            address_line2 = ' '
        
        city = request.POST['city']
        state = request.POST['state']
        postal_code=request.POST['postal_code']
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
        
        if User.objects.filter(email=email).exists():
            #message
            messages.error(request, 'Email already exists')
            #redirect to register page
            return redirect("accounts:register")
        
        #create user and profile
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        profile = Profile.objects.create(user=user, phone=phone, address=address, city=city, state=state, postal_code=postal_code, address_line2=address_line2)
        #add user to contact list
        contact_list=ContactList.objects.create(first_name=first_name,last_name=last_name,email=email,phone=phone,address=address)
        
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
    #get state , city if user have profile
        
    context={
        'state_choices':STATE_CHOICES,
        'user':user,
        'profile':myprofile,
    }
    
    if request.method=="POST":
        #get first_name , last_name  , phone , state , city , image , current_password , new_password 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        image = request.FILES.get('image',False)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        postal_code=request.POST['postal_code']
        #address
        address = request.POST['address']
        address_line2 = request.POST['address_line2']
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
            myprofile = Profile.objects.create(user=user, phone=phone, city=city, state=state, image=image, postal_code=postal_code, address=address, address_line2=address_line2)
        else:
            myprofile.phone=phone
            myprofile.state=state
            myprofile.city=city
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

    #get orders
    orders=Order.objects.filter(user=user)
    context={
        'state_choices':STATE_CHOICES,
        'country_choices':COUNTRY_CHOICES,
        'user':user,
        'profile':myprofile,
        'orders':orders,
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
    if request.method=="POST":
        #get email
        email=request.POST['email']
        #check if user exists
        if User.objects.filter(email=email).exists():
            #get user
            user=User.objects.get(email=email)
            subject="Reset Password"
            message="To reset your password click on this link https://furydgp.com/accounts/reset_password/"+str(user.id)
            email_from = settings.EMAIL_HOST_USER
            #send mail
            send_mail(
                subject,
                message,
                email_from,
                [email],
                fail_silently=False,
            )
            #message
            messages.success(request, 'Email sent successfully')
                
        else:
            #message
            messages.error(request, 'Email does not exist')
            #redirect to forgot password page
            return redirect("accounts:forgot_password")
            
    return render(request, 'forgetpassword.html', {})



def reset_password(request,id):
    #get user by id
    user=User.objects.get(id=id)
    #get password1 , password2
    if request.method=="POST":
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        #check if passwords match
        if password1 != password2:
            #message
            messages.error(request, 'Passwords do not match')
            #redirect to reset password page
            return redirect("accounts:reset_password",id=id)
        #set password
        user.set_password(password1)
        #save user
        user.save()
        #message
        messages.success(request, 'Password updated successfully')
        #redirect to login page
        return redirect("accounts:login")
    return render(request, 'resetePassword.html', {})