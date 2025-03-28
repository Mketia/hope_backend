from django.urls import path
from account.views import (
    register, 
    login, 
    logout, 
    request_reset_code, 
    verify_reset_code
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),  # ✅ Ensure login is not commented out
    path('logout/', logout, name='logout'),
    
    # ✅ Add password reset routes
    path('request-reset-code/', request_reset_code, name='request-reset-code'),
    path('verify-reset-code/', verify_reset_code, name='verify-reset-code'),
]
