from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUserSerializer , LoginSerializer , SendOTPSerializer ,VerifyOTPSerializer , UserSerializer , ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class CreateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            
            return Response(
                {'message': 'User created successfully.', 'data':serializer.data, 'refresh': str(refresh),
                'access': str(refresh.access_token),},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                user_data = UserSerializer(user).data
                tokens = serializer.get_tokens(user)
                return Response({
                    "message": "Login successful.",
                    "data":user_data,
                    "access": tokens['access_token'],
                    "refresh": tokens['refresh_token'],
                }, status=status.HTTP_200_OK)
            
            # If validation fails, return validation errors
            return Response({
                "message": "Login failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Catch-all for any unexpected server errors
            return Response({
                "message": "An unexpected error occurred.",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class SendVerifyEmailAPI(APIView):
    def get(self, request):
        user = request.user  # Get the authenticated user
        serializer = SendOTPSerializer()
        try:
            serializer.save(user)
            return Response({"message": "OTP email sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to send OTP email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except AuthenticationFailed as e:
            return Response(
                {"error": "Token has expired. Please refresh your token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            try:
                serializer.save(otp)
                return Response({"message": "OTP verified successfully. User is now verified."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"An unexpected error occurred. Please try again later.{e}",}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer()
        try:
            user = User.objects.get(email=request.data['email'])
            serializer.save(user,subject='Reset Your Password',template='mail/reset-password-otp.html')
            return Response({"message": "OTP sent to email successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class VerifyResetPasswordOTPAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            try:
                serializer.otp_delete(otp)
                return Response({"message": "OTP verified successfully. User can change password"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"An unexpected error occurred. Please try again later.{e}",}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been changed successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": f"An unexpected error occurred. Please try again later.{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)