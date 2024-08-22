from django.urls import path, include
from rest_framework import routers # type: ignore
from . import views 
from . import my_api_views


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
router.register(r'requests', views.RequestViewSet)
router.register(r'imageupload', views.ImageUploadViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('check-username/<str:username>/', my_api_views.check_username, name='check-username'),
    path('user-signup/', my_api_views.user_signup, name='user-signup'),
    path('requests/', my_api_views.show_requests, name='show-requests'),
    path('images/<str:purpose>/', my_api_views.get_all_images_for_user, name='get-all-images-for-user'),
    path('is-backer/', my_api_views.is_backer, name='is-backer'),
    path('jobs-near-me/', my_api_views.jobs_near_me, name='jobs-near-me'),
    path('request-detail-to-backer/<int:request_id>/', my_api_views.get_request_details_for_backer, name='request-detail-to-backer'),
]

