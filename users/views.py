from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from college.models import MasterCollege
from .models import CustomUser, College
from .serializers import SignupSerializer, LoginSerializer
from .authentication import SchemaAwareJWTAuthentication

from .util import extract_allotment_data

from rest_framework.parsers import MultiPartParser, FormParser


class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered. Please login."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                }
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UploadAndVerifyAllotmentAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [SchemaAwareJWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user

        file = request.FILES.get("allotment_pdf")
        if not file:
            return Response({"error": "Upload file under key 'allotment_pdf'."}, status=400)

        # Extract fields
        data = extract_allotment_data(file)
        print("DATA",data)

        counselling_id = data.get("counselling_id")
        department = data.get("department")

        if not counselling_id:
            return Response({"error": "Cannot detect counselling ID from PDF."}, status=400)

        # Validate MasterCollege
        try:
            master = MasterCollege.objects.get(counselling_id=counselling_id)
        except MasterCollege.DoesNotExist:
            return Response({
                "error": "Counselling ID not found in MasterCollege.",
                "counselling_id": counselling_id
            }, status=404)

        # Create UserCollege
        file.seek(0)
        user_college = College.objects.create(
            user=user,
            master_college=master,
            department=department,
            application_no=data.get("application_no"),
            counselling_number = counselling_id if counselling_id else ''
            # admission_no=data.get("admission_no"),
            # allotment_pdf=file
        )

        # Link user → user_college
        user.user_college = user_college
        user.is_verified = True
        user.save()

        return Response({
            "message": "Allotment verified successfully.",
            "college": {
                "name": master.name,
                "city": master.city,
                "state": master.state
            },
            "department": department,
            "application_no": data.get("application_no"),
            "admission_no": data.get("admission_no")
        })