from django.urls import path, include
from rest_framework import routers # type: ignore
from . import views 
from . import my_api_views 
from ecommerce import views as ecommerce_views


router = routers.DefaultRouter()

router.register(r'customusers', views.CustomUserViewSet)
router.register(r'pets', views.PetViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'backers', views.BackerViewSet)
router.register(r'availabilities', views.AvailabilityViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'messages', views.MessageViewSet)
router.register(r'messagedatas', views.MessageDataViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'shortrequests', views.ShortRequestViewSet)
# router.register(r'requests', views.RequestViewSet)
router.register(r'dogwalking_requests', views.DogWalkingRequestViewSet)
router.register(r'pettraining_requests', views.PetTrainingRequestViewSet)
router.register(r'petboarding_requests', views.PetBoardingRequestViewSet)
router.register(r'imageupload', views.ImageUploadViewSet)

# ecommerce views
router.register(r'categories', ecommerce_views.CategoryViewSet)
router.register(r'brands', ecommerce_views.BrandViewSet)
router.register(r'products', ecommerce_views.ProductViewSet)
router.register(r'productimages', ecommerce_views.ProductImageViewSet)
router.register(r'productvariants', ecommerce_views.ProductVariantViewSet)
router.register(r'pettypes', ecommerce_views.PetTypeViewSet)
router.register(r'breeds', ecommerce_views.BreedViewSet)
router.register(r'productpetcompatibilities', ecommerce_views.ProductPetCompatibilityViewSet)
router.register(r'orders', ecommerce_views.OrderViewSet)
router.register(r'orderitems', ecommerce_views.OrderItemViewSet)
router.register(r'wishlists', ecommerce_views.WishlistViewSet)
router.register(r'wishlistitems', ecommerce_views.WishlistItemViewSet)
router.register(r'ecommerce_reviews', ecommerce_views.EcommerceReviewViewSet)
router.register(r'addresses', ecommerce_views.AddressViewSet)
router.register(r'ecommerce_payments', ecommerce_views.EcommercePaymentViewSet)
router.register(r'discounts', ecommerce_views.DiscountViewSet)
router.register(r'promotions', ecommerce_views.PromotionViewSet)
router.register(r'petprofiles', ecommerce_views.PetProfileViewSet)
router.register(r'inventorylogs', ecommerce_views.InventoryLogViewSet)
router.register(r'stockalerts', ecommerce_views.StockAlertViewSet)
router.register(r'carts', ecommerce_views.CartViewSet)
router.register(r'cartitems', ecommerce_views.CartItemViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('check-username/<str:username>/', my_api_views.check_username, name='check-username'),
    path('user-signup/', my_api_views.user_signup, name='user-signup'),
    # path('requests/', my_api_views.show_requests, name='show-requests'),
    path('images/<str:purpose>/', my_api_views.get_all_images_for_user, name='get-all-images-for-user'),
    path('is-backer/', my_api_views.is_backer, name='is-backer'),
    path('requests/', my_api_views.show_requests_to_user, name='show-requests-to-user'),
    path('jobs-near-me/', my_api_views.jobs_near_me, name='jobs-near-me'),
]

