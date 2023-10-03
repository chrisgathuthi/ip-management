from django.urls import path
from rest_framework.authtoken import views
from .views import AllocateIP, ListAvailableIP, UpdateIp, CustomerInfoViewset
urlpatterns = [
    path("release/<str:address>/", UpdateIp.as_view(), name="release-ip"),
    path("available/",ListAvailableIP.as_view(),name="available-ip"),
    path("allocate/",AllocateIP.as_view(),name="allocate-ip"),
    path("allocated/",AllocateIP.as_view(),name="allocated-ip"),
    path("customer/<int:pk>/",CustomerInfoViewset.as_view(),name="customer-detail"),
    path("token/",views.obtain_auth_token, name="token")
]
