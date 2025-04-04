from django.urls import path
from account.views import (
    register, 
    login, 
    logout, 
    request_reset_code,
    set_new_password
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    
    path('request-reset-code/', request_reset_code, name='request-reset-code'),
    path('new-password/', set_new_password, name='set_new_password'),
]
