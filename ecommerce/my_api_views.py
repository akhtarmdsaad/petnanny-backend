from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from . import models 
from django.db.models import Avg
from . import serializers

# get all product of same category
@api_view(['GET'])
def get_products_by_category(request, category):
    category = models.Category.objects.get(name=category)
    products = models.Product.objects.filter(category=category)
    data = serializers.ProductSerializer(products, many=True)
    for product in data.data:
        product['image'] = models.ProductImage.objects.filter(product=product['id'],is_primary=True).first().image.url
    # add rating 
    for product in data.data:
        product['rating'] = models.EcommerceReview.objects.filter(product=product['id']).aggregate(Avg('rating'))['rating__avg']
    
    return Response({'products': data.data})

@api_view(['GET'])
def get_product_by_id(request, id):
    product = models.Product.objects.get(id=id)
    data = serializers.ProductSerializer(product)
    data = data.data
    data['images'] = serializers.ProductImageSerializer(models.ProductImage.objects.filter(product=data['id']), many=True).data
    # add rating 
    data['rating'] = models.EcommerceReview.objects.filter(product=data['id']).aggregate(Avg('rating'))['rating__avg']
    
    return Response({'product': data})