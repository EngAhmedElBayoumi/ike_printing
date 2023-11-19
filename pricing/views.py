from django.shortcuts import render
from .models import ProductDiscountQuantity , PrintingDiscountQuantity , PrintingPrice , GeneralDiscount , Copoun
from product.models import Product
#import json
import json
#import HttpResponse
from django.http import HttpResponse
#import Decimal
from decimal import Decimal
from django.db.models import Q
#import JsonResponse
from django.http import JsonResponse
# Create your views here.





def calculate_price(request):
    if request.method == 'GET':
        try:
            # Get data from the request
            product_data_str = request.GET.get('productData')

            # Parse the JSON data
            product_data = json.loads(product_data_str)

            # Extract data from product_data
            tshirt_height = Decimal(product_data.get('tshirtHeight', 0))
            front_design_height = Decimal(product_data.get('frontDesignHeight', 0))
            back_design_height = Decimal(product_data.get('backDesignHeight', 0))
            product_size = product_data.get('productSize', [])

            # Calculate product price
            product_price = calculate_product_price(product_size)
            # Calculate design price
            front_design_price = calculate_design_price(front_design_height,product_size,tshirt_height)
            back_design_price = calculate_design_price(back_design_height,product_size,tshirt_height)
            # Calculate total price
            total_price = product_price + front_design_price + back_design_price
            total_price = apply_additional_discounts(total_price)
            # Return the result as JSON
            result = {
                'success': True,
                'message': 'Price calculated successfully.',
                'totalPrice': total_price,
                'productPrice': product_price,
                'frontDesignPrice': front_design_price,
                'backDesignPrice': back_design_price,
            }
            return JsonResponse(result)
        except Exception as e:
            # Handle any exceptions
            result = {'success': False, 'message': str(e)}
            return JsonResponse(result)
    else:
        # Handle invalid request method
        result = {'success': False, 'message': 'Invalid request method.'}
        return JsonResponse(result)
    
    
    

# Helper function to calculate product price
def calculate_product_price(product_size):
    total_price = Decimal(0)
    # Assuming discounts are based on quantity
    for size in product_size:
        size_quantity = int(size.get('sizeQuantity', 0))
        size_price = Decimal(size.get('sizePrice', 0))
        # Check if there's any applicable discount for this quantity
        discount = get_discount_for_quantity(size_quantity)
        # Apply discount if applicable
        discounted_price = apply_discount(size_price, discount)
        # Calculate the total price for this size
        total_price += size_quantity * discounted_price
    return total_price

# Helper function to get applicable discount for a quantity
def get_discount_for_quantity(quantity):
    try:
        # Get the appropriate discount record from the database
        discount_quantity = ProductDiscountQuantity.objects.get(
            Q(min_quantity__lte=quantity) & Q(max_quantity__gte=quantity)
        )
        return discount_quantity.discount
    except ProductDiscountQuantity.DoesNotExist:
        return 0  # No discount found








# Helper function to calculate design price based on design height with pixels and tshirt size by inches , tshirt height by pixels
   
#i have in productSize (sizeQuantity , sizeHeight=> by inches , sizePrice) , tshirtHeight=>by pixel , frontDesignHeight => by pixel , backDesignHeight => by pixels
   
    
def calculate_design_price(design_height,product_size,tshirt_height):
    total_price = Decimal(0)
    # Assuming discounts are based on quantity
    for size in product_size:
        size_quantity = int(size.get('sizeQuantity', 0))
        size_height_by_inches = Decimal(size.get('sizeHeight', 0))
        design_height_by_pixels = Decimal(design_height)
        tshirt_height_by_pixels = Decimal(tshirt_height)
        #get design height by inches by dividing tsirt height by pixels by / size height by inches 
        design_height_by_inches = tshirt_height_by_pixels / size_height_by_inches
        #get design height by inches by dividing design height by pixels by / design height by inches
        design_height_by_inches = design_height_by_pixels / design_height_by_inches
        #get design price depend on design height by inches in  PrintingPrice table 
        design_price = PrintingPrice.objects.get(
            Q(min_height__lte=design_height_by_inches) & Q(max_height__gte=design_height_by_inches)
        )        
        
        # Check if there's any applicable discount for this quantity
        discount = get_discount_for_design_quantity(size_quantity)
        # Apply discount if applicable
        discounted_price = apply_discount(size_price, discount)
        # Calculate the total price for this size
        total_price += size_quantity * discounted_price
    return total_price


#helper function to get discount for design quantity
def get_discount_for_design_quantity(quantity):
    try:
        # Get the appropriate discount record from the database
        discount_quantity = PrintingDiscountQuantity.objects.get(
            Q(min_quantity__lte=quantity) & Q(max_quantity__gte=quantity)
        )
        return discount_quantity.discount
    except PrintingDiscountQuantity.DoesNotExist:
        return 0  # No discount found


# Helper function to apply additional discounts
def apply_additional_discounts(price):
    try:
        # Get the appropriate discount record from the database
        discount = GeneralDiscount.objects.get(pk=1)
        return apply_discount(price, discount.discount)
    except GeneralDiscount.DoesNotExist:
        return price  # No discount found
    
    

# Helper function to apply discount to a price
def apply_discount(price, discount):
    return price - (price * discount)