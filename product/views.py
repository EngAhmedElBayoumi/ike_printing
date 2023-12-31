from django.shortcuts import render
#get product , Matireal , color , size , category model
from .models import Product , Matireal , Color , Size , Category ,ClipArt ,UserImage ,ProductDesign ,FavoriteProduct ,CartProduct , CardSize , Order
from .models import DesignImage
from shipping.models import Shipping_price
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.serializers import serialize
from pricing.models import ProductDiscountQuantity ,PrintingDiscountQuantity ,PrintingPrice ,GeneralDiscount ,Copoun
#import login required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from paypal.standard.forms import PayPalPaymentsForm 
import uuid 
#redirect
from django.shortcuts import redirect
#settings
from django.conf import settings
#reverse
from django.urls import reverse
#django messages
from django.contrib import messages
#datetime
from datetime import datetime , timedelta
#import login_requried
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
import requests
import base64
import uuid

#import send mail
from django.core.mail import send_mail

# Create your views here.

def product(request):
    #get all products
    products = Product.objects.filter(is_active=True)
    #get all matireals
    matireals = Matireal.objects.all()
    #add artubute number to matireals to use it in template to display how many products have this matireal
    for matireal in matireals:
        matireal.number = Product.objects.filter(matireal=matireal).count()
    colors = Color.objects.all()
    #get all colors
    for color in colors:
        color.number = Product.objects.filter(colors=color).count()
        color.id=color.id
        color.code=color.code
        
    #get all sizes
    sizes = Size.objects.all()
    #add artubute number to sizes to use it in template to display how many products have this size
    for size in sizes:
        size.number = Product.objects.filter(sizes=size,is_active=True).count()
        size.id=size.id
    #get all categories
    categories = Category.objects.all()
    #add artubute number to categories to use it in template to display how many products have this category
    for category in categories:
        category.number = Product.objects.filter(category=category,is_active=True).count()
        
    #get size depend on simbol without duplicate
    sizes = Size.objects.values('simbol').distinct()
    
    #get color depend on code without duplicate
    colors = Color.objects.values('code').distinct()
    
    context={
        'products':products,
        'matireals':matireals,
        'colors':colors,
        'sizes':sizes,
        'categories':categories,
    }
    return render(request, 'products.html', context)


def product_with_category(request,category_id):
    
    #get  products by category id
    products = Product.objects.filter(is_active=True,category=category_id)
    #get all matireals
    matireals = Matireal.objects.all()
    #add artubute number to matireals to use it in template to display how many products have this matireal
    for matireal in matireals:
        matireal.number = Product.objects.filter(matireal=matireal).count()
    #get all colors
    colors = Color.objects.all()
    #get all sizes
    sizes = Size.objects.all()
    #add artubute number to sizes to use it in template to display how many products have this size
    for size in sizes:
        size.number = Product.objects.filter(sizes=size,is_active=True).count()
    #get all categories
    categories = Category.objects.all()
    #add artubute number to categories to use it in template to display how many products have this category
    for category in categories:
        category.number = Product.objects.filter(category=category,is_active=True).count()
        
    #get size depend on simbol without duplicate
    sizes = Size.objects.values('simbol').distinct()
    
    #get color depend on code without duplicate
    colors = Color.objects.values('code').distinct()
    
    context={
        'products':products,
        'matireals':matireals,
        'colors':colors,
        'sizes':sizes,
        'categories':categories,
    }
    return render(request, 'products.html', context)


@login_required()
def self_customization(request):
    #get all clip arts
    clip_arts = ClipArt.objects.all()
    #get all user images if user is authenticated
    if request.user.is_authenticated:
        user_images = UserImage.objects.filter(user=request.user)
        product_designs = ProductDesign.objects.filter(user=request.user)
    else:
        user_images = []
        product_designs=[]
    #get 2 products for each category
    categories = Category.objects.all()
    products = []
    for category in categories:
        #check if there are product has this category
        if Product.objects.filter(category=category,is_active=True).exists():
            products.append(Product.objects.filter(category=category,is_active=True).first())

        
    products_data = serialize('json', [p for p in products if p is not None]) 
    size_data = serialize('json', Size.objects.all())    
    
       
    #get related products that have the same category get first 10 products
    #check if products is not empty
    if products and products[0] is not None:
        related_products = Product.objects.filter(category=products[0].category,is_active=True).exclude(id=products[0].id).distinct()[:10]
    else:
        related_products = []
    
    
    context={
        'clip_arts':clip_arts,
        'user_images':user_images,
        'products':products,
        'product_designs':product_designs,
        'products_json': products_data,
        'sizes_json': size_data,
        'related_products': related_products,
    }
    
    return render(request, 'custom.html', context)

@login_required()
def self_customization_product(request,id):
    #get all clip arts
    clip_arts = ClipArt.objects.all()
    #get all user images if user is authenticated
    if request.user.is_authenticated:
        user_images = UserImage.objects.filter(user=request.user)
        product_designs = ProductDesign.objects.filter(user=request.user)
    else:
        user_images = []
        product_designs=[]
    #get 2 products for each category
    categories = Category.objects.all()
    products = []
    #get product by id
    product = Product.objects.get(id=id)
    #append product to products
    products.append(product)
    for category in categories:
        #check if there are product has this category
        if Product.objects.filter(category=category,is_active=True).exists():
            #check if product is not the same product
            if Product.objects.filter(category=category,is_active=True).first() != product:
                products.append(Product.objects.filter(category=category,is_active=True).first())
            
    products_data = serialize('json', [p for p in products if p is not None]) 
    size_data = serialize('json', Size.objects.all())    
    
       
    #get related products that have the same category get first 10 products
    #check if products is not empty
    if products and products[0] is not None:
        related_products = Product.objects.filter(category=products[0].category,is_active=True).exclude(id=products[0].id).distinct()[:10]
    else:
        related_products = []
    
    
    context={
        'clip_arts':clip_arts,
        'user_images':user_images,
        'products':products,
        'product_designs':product_designs,
        'products_json': products_data,
        'sizes_json': size_data,
        'related_products': related_products,
    }
    
    return render(request, 'custom.html', context)



def edit_product_design(request,product_id):
    #get product by id
    product = Product.objects.get(id=product_id)
    #get all clip arts
    clip_arts = ClipArt.objects.all()
    #get all user images if user is authenticated
    if request.user.is_authenticated:
        user_images = UserImage.objects.filter(user=request.user)
    else:
        user_images = []
    #get 2 products for each category
    categories = Category.objects.all()
    products = []
    #append product to products
    products.append(product)
    for category in categories:
        products.append(Product.objects.filter(category=category).first())
        products.append(Product.objects.filter(category=category).last())
    context={
        'clip_arts':clip_arts,
        'user_images':user_images,
        'products':products,
    }
    
    return render(request, 'custom.html', context)



def ordaring(request):
    #get user
    if request.user.is_authenticated:
        user=request.user
        orders=Order.objects.filter(user=user)
    else:
        orders=[]
    return render(request, 'Ordaring.html', {'orders':orders})



def getproductsbycategory(request, category_name):
    # Get category by name
    category = Category.objects.get(name=category_name)
    # Get products by category
    products = Product.objects.filter(category=category,is_active=True)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
            "id": product.id,
        })
    
    return JsonResponse({"products": product_data})


##getproductsbysize name
def getproductsbysize(request,size_id):
    # Get size by name
    size = Size.objects.get(id=size_id)
    # Get products by size
    products = Product.objects.filter(sizes=size,is_active=True)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
            "id": product.id,
        })
    return JsonResponse({"products": product_data})


##getproductsbymatireal name
def getproductsbymatireal(request,matireal_name):
    # Get matireal by name
    matireal = Matireal.objects.get(name=matireal_name)
    # Get products by matireal
    products = Product.objects.filter(matireal=matireal,is_active=True)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
            "id": product.id,
        })
    
    return JsonResponse({"products": product_data})
    
    
##getproductsbycolor name
def getproductsbycolor(request,color_id):
    # Get color by name
    color = Color.objects.get(id=color_id)
    # Get products by color
    products = Product.objects.filter(colors=color,is_active=True)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
            "id": product.id,
        })
    
    return JsonResponse({"products": product_data})


#save user image
def save_user_image(request):
    #check if user is authenticated
    if not request.user.is_authenticated:
        #return error
        return JsonResponse({"error":"user not authenticated"})
    #get user
    user=request.user
    #get image
    image=request.FILES['image']
    #name = image name
    name=image.name
    #save image
    userimage=UserImage.objects.create(user=user,name=name,image=image)
    #return image url
    return JsonResponse({"image_url":userimage.image.url}) 



def getproductbyid(request, product_id):
    #get product by id
    product = Product.objects.get(id=product_id,is_active=True)
    #get product sizes
    if product:
        sizes = product.sizes.all()
        #get product colors
        colors = product.colors.all()
        #get product matireal
        matireal = product.matireal.all()
        description=product.description
    else:
        sizes = []
        colors = []
        matireal = []
        description=""
    
    #related products
    related_products = Product.objects.filter(category=product.category,is_active=True).exclude(id=product.id).distinct()[:10]
    
    #get product data
    product_data = {
        #size , color , matireal
        "sizes": serializers.serialize('json', sizes),
        "colors": serializers.serialize('json', colors),
        "matireals": serializers.serialize('json', matireal),
        "description": description,
        "height": product.height,
        "related_products": serializers.serialize('json', related_products),
        "id": product_id,
    }
    
    return JsonResponse({"product": product_data})


#save ProductDesign send in request data contain front , back 
def save_design(request):
    try:
        if request.method == "POST":
            #check if user is authenticated
            if not request.user.is_authenticated:
                #return error
                return JsonResponse({"error":"user not authenticated"})
            #get user
            user=request.user
            front_data = json.loads(request.POST.get('front'))
            back_data = json.loads(request.POST.get('back'))
            front_canvas_data = request.POST.get('frontcanvas')
            name = request.POST.get('name')
            csrf_token = request.POST.get('csrfmiddlewaretoken')
            #create product design
             # Create product design
            product_design = ProductDesign.objects.create(name=name, frontcanvas=front_data, backcanvas=back_data, frontimage=front_canvas_data)
            # Set user
            product_design.user.set([user])

            # Save canvas data using set_frontcanvas and set_backcanvas
            product_design.set_frontcanvas()
            product_design.set_backcanvas()
            product_design.save()
            
            #convert product design to json
            product_design_data = {
                "product_design": serializers.serialize('json', [product_design]),
            }
            #return product design data
            return JsonResponse({"product_design": product_design_data})
              
            
           
        


        
    except Exception as e:
        return JsonResponse({"error": str(e)})
        



#get all user product design
def get_user_product_design(request):
    #check if user is authenticated
    if not request.user.is_authenticated:
        #return error
        return JsonResponse({"error":"user not authenticated"})
    #get user
    user=request.user
    #get user product design
    product_designs = ProductDesign.objects.filter(user=user)
    #get product design data
    product_designs_data = {
        "product_designs": serializers.serialize('json', product_designs), 
    }
    # Construct a list of product design data to return as JSON

    
    #return product design data
    return JsonResponse({"product_designs": product_designs_data})



#validate positive integer
def validate_positive_integer(value, field_name):
    try:
        validated_value = int(value)
        if validated_value < 0:
            raise ValueError(f"{field_name} should be a positive integer.")
        return validated_value
    except ValueError:
        raise ValueError(f"{field_name} should be a valid positive integer.")

#front and back design price
def get_front_back_design_price(front_design_height, back_design_height, quantity):
    #convert quantity to decimal
    quantity = validate_positive_integer(quantity, "Quantity")
        
    # Validate and set default values if height is null
    front_design_height = validate_positive_integer(front_design_height, "Front Design Height") or 0
    back_design_height = validate_positive_integer(back_design_height, "Back Design Height") or 0

    # Get front and back design prices
    if front_design_height != 0 :
        front_design_price = PrintingPrice.objects.filter(min_size__lte=front_design_height, max_size__gte=front_design_height).first()
    else:
        front_design_price = 0
    if front_design_price:
        front_design_price=front_design_price.price * quantity
        
    else:
        front_design_price=0
    
    if back_design_height != 0 :
        back_design_price = PrintingPrice.objects.filter(min_size__lte=back_design_height, max_size__gte=back_design_height).first()
    else:
        back_design_price = 0
    
    if back_design_price:  
         
        back_design_price=back_design_price.price * quantity
    else:
        back_design_price=0
    

    return front_design_price, back_design_price

#general discount
def get_general_discounted_price(total_price):
    # Get and apply general discount
    general_discount = GeneralDiscount.objects.first()
    if general_discount:
        general_discount = general_discount.discount
        total_price -= total_price * (general_discount / 100)

    return total_price

#printing discount depend on quantity
def get_printing_discounted_price(quantity, design_price):
    # Get and apply printing discount
    printing_discount = PrintingDiscountQuantity.objects.filter(min_quantity__lte=quantity, max_quantity__gte=quantity).first()
    if printing_discount:
        printing_discount = printing_discount.discount
        design_price -= design_price * (printing_discount / 100)

    return design_price

#quantity discount
def get_quantity_discounted_price(quantity, quantity_price):
    # Get and apply quantity discount
    quantity_discount = ProductDiscountQuantity.objects.filter(min_quantity__lte=quantity, max_quantity__gte=quantity).first()
    if quantity_discount:
        quantity_discount = quantity_discount.discount
        quantity_price -= quantity_price * (quantity_discount / 100)

    return quantity_price

def get_quote(request):
    front_design_height = request.POST.get('front_design_height')
    back_design_height = request.POST.get('back_design_height')
    quantity = request.POST.get('quantity')
    quantity_price = request.POST.get('quantity_price')
    
    try:
        # Validate and get front, back, and quantity prices
        front_design_price, back_design_price = get_front_back_design_price(
            front_design_height, back_design_height, quantity
        )

        # Convert to int and float
        quantity = validate_positive_integer(quantity, "Quantity")
        front_design_price = float(front_design_price)
        back_design_price = float(back_design_price)
        quantity_price = float(quantity_price)

        #Apply printing discount
        front_design_price = get_printing_discounted_price(quantity, front_design_price)
        back_design_price = get_printing_discounted_price(quantity, back_design_price)

        # Apply quantity discount
        total_price_quantity = get_quantity_discounted_price(quantity, quantity_price)

        # Calculate total price
        total_price = front_design_price + back_design_price + total_price_quantity

        # Apply general discount
        total_price = get_general_discounted_price(total_price)
        # Create JSON data
        data = {
            "front_design_price": front_design_price,
            "back_design_price": back_design_price,
            "quantity_price": quantity_price,
            "total_price": total_price,
        }
        return JsonResponse(data)

    except ValueError as e:
        return JsonResponse({"error": str(e)})
    
    
#apply copoun
def apply_copoun(request):
    #get copoun code
    copoun_code=request.POST.get('copoun_code')
    #get copoun
    copoun=Copoun.objects.filter(copoun_name=copoun_code).first()
        #get total price
    total_price_str=request.POST.get('total_price')
    #convert total price to float
    total_price=float(total_price_str)
    #check if copoun is null
    if copoun == None:
        #return error
        return JsonResponse({"total_price":total_price})
    #get copoun discount
    copoun_discount=copoun.discount


    #apply discount
    total_price=total_price-(total_price*(copoun_discount/100))
    #return total price
    return JsonResponse({"total_price":total_price})
    
    

def order(request):
    # Get product card
    product_card = CartProduct.objects.filter(user=request.user)
    #get total price from session
    total_price = request.session['total_price']    
    
    #get methods of receiving
    method_of_receiving = request.POST.get('method_of_receiving_input')
    if method_of_receiving == "delivery":
        total_price += 20
        #put total price in session
        request.session['total_price'] = total_price
        
    if method_of_receiving == "Shipping":
        #get shipping price
        shipping_price = Shipping_price.objects.first()
        #check if shipping price is null
        if shipping_price == None:  
            total_price += 0
        else:
            #get shipping price
            shipping_price = shipping_price.price
            #add shipping price to total price
            total_price += shipping_price
        #put total price in session
        request.session['total_price'] = total_price

    #put all data in session and return redirct page
    request.session['product_card'] = list(product_card.values())
    request.session['method_of_receiving'] = method_of_receiving
    
    return redirect('product:order_page')

    

    # Return error if something went wrong
    return JsonResponse({"error": "error"})
 
def order_page(request):
    #get product card
    product_card = request.session['product_card']
    #get total price
    total_price = request.session['total_price']
    host = request.get_host() # Host 
    paypal_checkout = {
            'business' : settings.PAYPAL_RECEIVER, 
            'amount' : total_price, 
            'item_name' : 'payment for card products', 
            'invoice' : uuid.uuid4(), 
            'currency' : 'USD', 
            'notify_url' : f'http://{host}{reverse("paypal-ipn")}/',
            'return_url' : f'http://{host}{reverse("product:payment_success")}',
            'cancel_url' : f'http://{host}{reverse("product:payment_failed")}',
    }  
    
    paypal = PayPalPaymentsForm(initial=paypal_checkout)
    
    return render(request, 'order_redirect.html', {'product_card':product_card,'total_price':total_price,'paypal':paypal})
  
  
#payment success
def payment_success(request):
    # Get product card
    product_card = CartProduct.objects.filter(user=request.user)
    #get user email
    user_email=request.user.email
    
    # Get total price from session
    total_price = request.session['total_price']
    method_of_receiving = request.session['method_of_receiving']
    #receiving date depend on method of receiving pickup or delivery 1 week if shipping 2 weeks
    if method_of_receiving == "pickup" or method_of_receiving == "delivery":
        receiving_date = datetime.now() + timedelta(days=7)
    else:
        receiving_date = datetime.now() + timedelta(days=14)

    # Use a transaction to ensure data consistency
    with transaction.atomic():
        # Create a new order
        order = Order.objects.create(user=request.user, total_price=total_price,methods_of_receiving=method_of_receiving,order_receiving_date=receiving_date)

        # Add products to the order
        order.cart_product.set(product_card)
        #get order id
        order_id=order.id
        
        
        # Clear the user field in each product_card
        for product in product_card:
            product.user.remove(request.user)

    #clear session
    request.session['product_card'] = []
    request.session['total_price'] = 0
    #send mail
    send_mail(
            'Order Confirmation',
            f'Your order has been placed successfully. with number #{order_id} and total price {total_price} and receiving date {receiving_date} and method of receiving {method_of_receiving}',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    #django messages
    messages.success(request, "Your order has been placed successfully.")
    
    #return redirect to card
    return redirect('product:card')


#payment failed
def payment_failed(request):
    #clear session
    request.session['product_card'] = []
    request.session['total_price'] = 0
    
    #django messages
    messages.error(request, "Your order has been failed try again.")
    
    #return redirect to card
    return redirect('product:card')
 

    
 
 
#login required
@login_required() 
def card(request):
    #get product card
    product_card = CartProduct.objects.filter(user=request.user)
    #shipping price
    shipping_price = Shipping_price.objects.first()
    #check if shipping price is null
    if shipping_price == None:
        shipping_price=0
    else:
        shipping_price=shipping_price.price
        
    #calculate total price
    subtotal=0
    for product in product_card:
        subtotal+=product.total_price
        
    tax = subtotal * 8.25 / 100
    transaction_fee = subtotal * 2.9 / 100 + 0.3
    if subtotal == 0:
        tax = 0
        transaction_fee = 0

    total_price = subtotal + tax + transaction_fee
    #append total price to product card
    product_card.subtotal=subtotal
    product_card.tax=tax
    product_card.transaction_fee=transaction_fee
    product_card.total_price=total_price  
    #put total price in session
    request.session['total_price'] = total_price
    
    #if request is post 
    if request.method == "POST":
        try:
            #get product id , quantity , front_design_price , back_design_price , quantity_price , total_price , frontcanvas , backcanvas
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            front_design_price = request.POST.get('front_design_price')
            back_design_price = request.POST.get('back_design_price')
            quantity_price = request.POST.get('quantity_price')
            total_price = request.POST.get('total_price')
            frontcanvas = request.POST.get('frontcanvas')
            backcanvas = request.POST.get('backcanvas')
            canvasBackgroundColor=request.POST.get('canvasBackgroundColor')
            #get size array
            size_array = request.POST.get('size')
            #get front_tshirt_image , back_tshirt_image
            front_tshirt_image = request.POST.get('front_tshirt_image')
            back_tshirt_image = request.POST.get('back_tshirt_image')
            #save design images
            design_images = request.POST.get('design_resource')
            design_images = json.loads(design_images)
            
            #check if canvasBackgroundColor is null
            if canvasBackgroundColor == "":
                #assign white to canvasBackgroundColor
                canvasBackgroundColor="#ffffff"
            
            # Convert the JSON string to a Python list
            size_data = json.loads(size_array)

            # Create a list to store size objects
            sizes = []

            # Loop through the size_data and create Size objects
            for size_item in size_data:
                symbol = size_item.get('symbol')
                size_quantity = size_item.get('quality')
                size = CardSize.objects.create(symbol=symbol, quantity=size_quantity)
                sizes.append(size)
           
           
            #get product
            product = Product.objects.get(id=product_id)
            #get user
            user=request.user
            #create cart product
            cart_product = CartProduct.objects.create( product=product, quantity=quantity, front_design_price=front_design_price, back_design_price=back_design_price, quantity_price=quantity_price, total_price=total_price, frontcanvas=frontcanvas, backcanvas=backcanvas,product_color=canvasBackgroundColor,front_tshirt_image=front_tshirt_image,back_tshirt_image=back_tshirt_image)
            #set user
            cart_product.user.set([user])
            #set sizes
            cart_product.sizes.set(sizes)  
            #loop on design images and create design image
            for design_image_data in design_images:
                design_image = DesignImage.objects.create(image=design_image_data)
                #add design image to cart product
                cart_product.design_images.add(design_image)

                    
                
            
            
            #save cart product
            cart_product.save()            
            #return success
            return JsonResponse({"success": "success"})
        except Exception as e:
            #return error
            return JsonResponse({"error": str(e)})
    return render(request, 'card.html', {'product_card':product_card,'shipping_price':shipping_price})


#remove from card
def remove_from_card(request,id):
    #get product
    product = Product.objects.get(id=id)
    #get user
    user=request.user
    #get cart product
    cart_product = CartProduct.objects.filter(product=product,user=user).first()
    #delete cart product
    cart_product.delete()
    #return success
    return JsonResponse({"success": "success"})

#crear card 
def clear_card(request):
    user=request.user
    
    cart_product = CartProduct.objects.filter(user=user).first()
    #delete cart product
    if cart_product:
        cart_product.delete()
    
    #return success
    return JsonResponse({"success": "success"})


