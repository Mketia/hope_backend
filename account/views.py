from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from account.services.account import VisitorService
from .models import ResetCode

User = get_user_model()
visitor_service = VisitorService()


@api_view(['POST'])
def register(request):
    try:
        response = visitor_service.create_visitor(request.data)
        if not response.success:
            return Response(response.message, status=response.status)
        return Response(response.data, status=response.status)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def login(request):
    try:
        response = visitor_service.login_visitor(request.data)
        if not response.success:
            return Response(response.message, status=response.status)
        return Response(response.data, status=response.status)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        response = visitor_service.logout_visitor(request.data)
        if not response.success:
            return Response(response.message, status=response.status)
        return Response(response.message, status=response.status)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ✅ New Endpoint to Generate Reset Code
@api_view(['POST'])
def request_reset_code(request):
    """Generates a reset code for the given user."""
    email = request.data.get("email")
    
    if not email:
        return Response({"error": "Email is required"}, status=400)
    
    try:
        user = User.objects.get(email=email)
        code = ResetCode.generate_reset_code(user)
        return Response({"message": "Reset code generated successfully", "code": code})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# ✅ New Endpoint to Verify Reset Code
@api_view(['POST'])
def verify_reset_code(request):
    """Verifies if the provided reset code is correct."""
    email = request.data.get("email")
    code = request.data.get("code")

    if not email or not code:
        return Response({"error": "Email and code are required"}, status=400)

    try:
        user = User.objects.get(email=email)
        reset_entry = ResetCode.objects.filter(user=user, code=code).first()

        if reset_entry:
            return Response({"message": "Reset code is valid"})
        else:
            return Response({"error": "Invalid reset code"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
