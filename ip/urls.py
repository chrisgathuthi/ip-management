from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path
from rest_framework.authtoken import views
from .views import AllocateIP, ListAvailableIP, UpdateIp,  SubnetCalculator, AllocatedIpView, Registrationviewset
urlpatterns = [
    path("release/<str:address>/", UpdateIp.as_view(), name="release-ip"),
    path("available/",ListAvailableIP.as_view(),name="available-ip"),
    path("allocate/",AllocateIP.as_view(),name="allocate-ip"),
    path("allocated/",AllocatedIpView.as_view(),name="allocated-ip"),
    path("subnetcalculator/",SubnetCalculator.as_view(),name="subnet-calculator"),
    path("token/",views.obtain_auth_token, name="token"),
    path("registration/",Registrationviewset.as_view(), name="registration"),
    path("schema/",SpectacularAPIView.as_view(),name="schema"),
    path("schema/docs/",SpectacularSwaggerView.as_view(),name="docs")
]
