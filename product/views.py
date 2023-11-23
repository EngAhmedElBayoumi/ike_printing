from django.shortcuts import render
#get product , Matireal , color , size , category model
from .models import Product , Matireal , Color , Size , Category ,ClipArt ,UserImage ,ProductDesign ,FavoriteProduct ,CartProduct
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.serializers import serialize

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


