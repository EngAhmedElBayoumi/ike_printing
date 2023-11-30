from django.shortcuts import render
#get product , Matireal , color , size , category model
from .models import Product , Matireal , Color , Size , Category ,ClipArt ,UserImage ,ProductDesign ,FavoriteProduct ,CartProduct
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.serializers import serialize
from pricing.models import ProductDiscountQuantity ,PrintingDiscountQuantity ,PrintingPrice ,GeneralDiscount ,Copoun
#import login required
from django.contrib.auth.decorators import login_required
# Create your views here.

def product(request):
    #get all products
    products = Product.objects.all()
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
        size.number = Product.objects.filter(sizes=size).count()
    #get all categories
    categories = Category.objects.all()
    #add artubute number to categories to use it in template to display how many products have this category
    for category in categories:
        category.number = Product.objects.filter(category=category).count()
    
    context={
        'products':products,
        'matireals':matireals,
        'colors':colors,
        'sizes':sizes,
        'categories':categories,
    }
    return render(request, 'products.html', context)




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
        products.append(Product.objects.filter(category=category).first())

        
    products_data = serialize('json', products)
    size_data = serialize('json', Size.objects.all())    
    
       
    #get related products that have the same category get first 10 products
    #check if products is not empty
    if products:
        related_products = Product.objects.filter(category=products[0].category).exclude(id=products[0].id).distinct()[:10]
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
    return render(request, 'Ordaring.html', {})



def getproductsbycategory(request, category_name):
    # Get category by name
    category = Category.objects.get(name=category_name)
    # Get products by category
    products = Product.objects.filter(category=category)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
        })
    
    return JsonResponse({"products": product_data})


##getproductsbysize name
def getproductsbysize(request,size_name):
    # Get size by name
    size = Size.objects.get(name=size_name)
    # Get products by size
    products = Product.objects.filter(sizes=size)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
        })
        
    return JsonResponse({"products": product_data})


##getproductsbymatireal name
def getproductsbymatireal(request,matireal_name):
    # Get matireal by name
    matireal = Matireal.objects.get(name=matireal_name)
    # Get products by matireal
    products = Product.objects.filter(matireal=matireal)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
        })
    
    return JsonResponse({"products": product_data})
    
    
##getproductsbycolor name
def getproductsbycolor(request,color_name):
    # Get color by name
    color = Color.objects.get(name=color_name)
    # Get products by color
    products = Product.objects.filter(colors=color)
    # Construct a list of product data to return as JSON
    product_data = []
    for product in products:
        product_data.append({
            "name": product.name,
            "description": product.description,
            "price": 0,
            "frontimage": product.frontimage.url,
            "backimage": product.backimage.url,
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
    #check image name if exist 
    if UserImage.objects.filter(name=name).exists():
        #return error
        return JsonResponse({"error":"image name exist"})
    #save image
    userimage=UserImage.objects.create(user=user,name=name,image=image)
    #return image url
    return JsonResponse({"image_url":userimage.image.url}) 



def getproductbyid(request, product_id):
    #get product by id
    product = Product.objects.get(id=product_id)
    #get product sizes
    sizes = product.sizes.all()
    #get product colors
    colors = product.colors.all()
    #get product matireal
    matireal = product.matireal.all()
    description=product.description
    
    #related products
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id).distinct()[:10]
    
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
            product_design = ProductDesign.objects.create(user=user, name=name, frontcanvas=front_data, backcanvas=back_data, frontimage=front_canvas_data)

            # Save canvas data using set_frontcanvas and set_backcanvas
            product_design.set_frontcanvas()
            product_design.set_backcanvas()
            product_design.save()

           
           
            #return product design id
            return JsonResponse({"product_design_id": product_design.id})
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



# def get_quote(request):
#     #get form front_design_height , back_design_height , quantity ,quantity_price
#     front_design_height = request.POST.get('front_design_height')
#     back_design_height = request.POST.get('back_design_height')
#     quantity = request.POST.get('quantity')
#     quantity_price = request.POST.get('quantity_price')
#     #check if quantity is 0 or null
#     if quantity == "0" or quantity == "":
#         #return error
#         return JsonResponse({"error":"quantity is 0"})
    
#     #get price for design depend on height
#     front_design_price = PrintingPrice.objects.filter(min_size__lte=front_design_height, max_size__gte=front_design_height).first()
#     #check if front_design_price is null
#     if front_design_price == None:
#         #return error
#         return JsonResponse({"error":"front design price not found"})
#     front_design_price=front_design_price.price
#     back_design_price = PrintingPrice.objects.filter(min_size__lte=back_design_height, max_size__gte=back_design_height).first()
#     #check if back_design_price is null
#     if back_design_price == None:
#         #return error
#         return JsonResponse({"error":"back design price not found"})
#     back_design_price=back_design_price.price
    
#     #----------------
#     #get discount for design depend on quantity
#     front_design_discount = PrintingDiscountQuantity.objects.filter(min_quantity__lte=quantity, max_quantity__gte=quantity).first()
#     #check if there are discount for front design
#     if front_design_discount:
#         front_design_discount=front_design_discount.discount
#         #apply discount
#         front_design_price=front_design_price-(front_design_price*(front_design_discount/100))
    
#     back_design_discount = PrintingDiscountQuantity.objects.filter(min_quantity__lte=quantity, max_quantity__gte=quantity).first()
#     #check if there are discount for back design
#     if back_design_discount:
#         back_design_discount=back_design_discount.discount
#         #apply discount
#         back_design_price=back_design_price-(back_design_price*(back_design_discount/100))
        
#     #----------------
#     #get discount for quantity
#     quantity_discount = ProductDiscountQuantity.objects.filter(min_quantity__lte=quantity, max_quantity__gte=quantity).first()
#     #check if there are discount for quantity
#     if quantity_discount:
#         quantity_discount=quantity_discount.discount
#         #apply discount
#         quantity_price=quantity_price-(quantity_price*(quantity_discount/100))
        
#     #----------------
#     #convert quantity , front_design_price , back_design_price to int
#     quantity=int(quantity)
#     front_design_price=float(front_design_price)
#     back_design_price=float(back_design_price)
#     quantity_price=float(quantity_price)
#     total_price = front_design_price + back_design_price + quantity_price
    
#     #----------------
#     #get general discount
#     general_discount = GeneralDiscount.objects.first()
#     #check if there are general discount
#     if general_discount:
#         general_discount=general_discount.discount
#         #apply discount
#         total_price=total_price-(total_price*(general_discount/100))
        
#     #create json data with front_design_price , back_design_price , quantity_price , total_price
#     data = {
#         "front_design_price": front_design_price,
#         "back_design_price": back_design_price,
#         "quantity_price": quantity_price,
#         "total_price": total_price,
#     }
#     if request.method=="POST":
#         #return data
#         print(data)
#         return JsonResponse(data)
    
#     #return data
#     return JsonResponse(data)
# #------------------------------



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
    front_design_price = PrintingPrice.objects.filter(min_size__lte=front_design_height, max_size__gte=front_design_height).first()
    if front_design_price:
        front_design_price=front_design_price.price * quantity
    else:
        front_design_price=0
    back_design_price = PrintingPrice.objects.filter(min_size__lte=back_design_height, max_size__gte=back_design_height).first()
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
        print(data)


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
    
    
    
#login required
@login_required() 
def card(request):
    #get product card
    product_card = CartProduct.objects.filter(user=request.user)
    
    #calculate total price
    total_price=0
    for product in product_card:
        total_price+=product.total_price
        
    #append total price to product card
    product_card.total=total_price
    
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
            #get product
            product = Product.objects.get(id=product_id)
            #get user
            user=request.user
            #create cart product
            cart_product = CartProduct.objects.create(user=user, product=product, quantity=quantity, front_design_price=front_design_price, back_design_price=back_design_price, quantity_price=quantity_price, total_price=total_price, frontcanvas=frontcanvas, backcanvas=backcanvas,product_color=canvasBackgroundColor)
            #return success
            return JsonResponse({"success": "success"})
        except Exception as e:
            #return error
            return JsonResponse({"error": str(e)})

    return render(request, 'card.html', {'product_card':product_card})
