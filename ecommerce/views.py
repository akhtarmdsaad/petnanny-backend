from django.shortcuts import render
from rest_framework import viewsets 
from .models import Category, Brand, Product, ProductImage, ProductVariant, PetType, Breed, ProductPetCompatibility, Order, OrderItem, Wishlist, WishlistItem, EcommerceReview, Address, EcommercePayment, Discount, Promotion, PetProfile, InventoryLog, StockAlert, Cart, CartItem 
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, ProductImageSerializer, ProductVariantSerializer, PetTypeSerializer, BreedSerializer, ProductPetCompatibilitySerializer, OrderSerializer, OrderItemSerializer, WishlistSerializer, WishlistItemSerializer, EcommerceReviewSerializer, AddressSerializer, EcommercePaymentSerializer, DiscountSerializer, PromotionSerializer, PetProfileSerializer, InventoryLogSerializer, StockAlertSerializer, CartSerializer, CartItemSerializer

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    
class PetTypeViewSet(viewsets.ModelViewSet):
    queryset = PetType.objects.all()
    serializer_class = PetTypeSerializer
    
class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    
class ProductPetCompatibilityViewSet(viewsets.ModelViewSet):
    queryset = ProductPetCompatibility.objects.all()
    serializer_class = ProductPetCompatibilitySerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    
class EcommerceReviewViewSet(viewsets.ModelViewSet):
    queryset = EcommerceReview.objects.all()
    serializer_class = EcommerceReviewSerializer
    
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
class EcommercePaymentViewSet(viewsets.ModelViewSet):
    queryset = EcommercePayment.objects.all()
    serializer_class = EcommercePaymentSerializer
    
class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    
class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    
class PetProfileViewSet(viewsets.ModelViewSet):
    queryset = PetProfile.objects.all()
    serializer_class = PetProfileSerializer
    
class InventoryLogViewSet(viewsets.ModelViewSet):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer  
    
class StockAlertViewSet(viewsets.ModelViewSet):
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    