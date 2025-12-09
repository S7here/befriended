from django.urls import path
from .views import SignupAPIView, LoginAPIView, UploadAndVerifyAllotmentAPIView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/',SignupAPIView.as_view(), name='signup'),
    path('login/',LoginAPIView.as_view(), name= 'login'),
    path("upload/verify-allotment/", UploadAndVerifyAllotmentAPIView.as_view()),
]