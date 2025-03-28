from account.models import Visitor
from account.repository.account import VisitorRepository
from base.utils.response import APIResponse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


visitor_repository = VisitorRepository()


class VisitorService:
    def create_visitor(self, data):
        try:
            required_fields = ["email","first_name","last_name","password","phone_number"]
            if not all(field in data for field in required_fields):
                return APIResponse(
                    success=False,
                    data=None,
                    message="Missing required fields",
                    status=status.HTTP_400_BAD_REQUEST
                    )
            existing_user = User.objects.filter(email=data.get('email'))
            if existing_user.exists():
                return APIResponse(
                    success=False,
                    data=None,
                    message="Visitor with this email already exists",
                    status=status.HTTP_400_BAD_REQUEST
                    )
            user = User.objects.create_user(
                username=data.get('email'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                password=data.get('password'),
            )
            response = visitor_repository.create_visitor(user=user, phone_number=data.get("phone_number"))

            if not response.success:
                return APIResponse(
                    success=False,
                    data=None,
                    message=response.message,
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return APIResponse(
                success=True,
                data=response.data,
                message=response.message,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"An error occured: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def logout_visitor(self, data):
        try:
            # Check if refresh token is provided in the request data
            if 'refresh' not in data:
                return APIResponse(
                    success=False,
                    data=None,
                    message="Refresh token is required",
                    status=400
                )

            # Get the refresh token from request data
            refresh_token = data['refresh']

            # Create token object and blacklist it
            token = RefreshToken(refresh_token)
            token.blacklist()

            return APIResponse(
                success=True,
                data=None,
                message={"message": "Successfully logged out"},
                status=200
            )

        except TokenError:
            return APIResponse(
                success=False,
                data=None,
                message="Invalid or expired token",
                status=400
            )
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Logout failed: {str(e)}",
                status=500
            )