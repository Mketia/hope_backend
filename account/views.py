from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from account.services.account import VisitorService
from base.email import EmailService
from base.models import ResetCode

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
        send_email = EmailService()
        subject = "Password Reset Code"
        text_body = f"Hi,\n\nYour reset code is: {code}\n\nIf you did not request this, please ignore this email."
        html_body = f"""
        <p>Hi,</p>
        <p>We received a request to reset your password. Your reset code is:</p>
        <h2>{code}</h2>
        <p>Please enter this code in the password reset form to continue.</p>
        <p>If you did not request this, please ignore this email. Your account remains secure.</p>
        <br>
        <p>Best,<br>Hope for Children Foundation Team</p>
        """
        send_email.send_email(email, subject, text_body, html_body)
        return Response({"message": "Reset code generated successfully", "code": code})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def set_new_password(request):
    """Verifies the reset code and updates the user's password."""
    email = request.data.get("email")
    code = request.data.get("code")
    new_password = request.data.get("new_password")

    if not email or not code or not new_password:
        return Response({"error": "Email, code, and new password are required"}, status=400)

    try:
        user = User.objects.get(email=email)
        reset_entry = ResetCode.objects.filter(user=user, code=code).first()

        if not reset_entry:
            return Response({"error": "Invalid reset code"}, status=400)

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Delete the reset code after successful password reset
        reset_entry.delete()

        return Response({"message": "Password reset successfully"})
    
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

