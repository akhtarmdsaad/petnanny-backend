from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [
        ProductImageInline,
    ]
admin.site.register(Product, ProductAdmin)
admin.site.register(PetType)
admin.site.register(ProductPetCompatibility)
admin.site.register(Breed)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Address)
admin.site.register(EcommercePayment)
admin.site.register(EcommerceReview)
admin.site.register(Discount)
admin.site.register(Promotion)
admin.site.register(PetProfile)
admin.site.register(InventoryLog)
admin.site.register(StockAlert)