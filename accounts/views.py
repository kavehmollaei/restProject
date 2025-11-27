from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serilaizers import  RegistrationSerilaizer
from rest_framework.response import Response
# Create your views here.

def sample(request,category):
    return HttpResponse(f"Showing products in category: {category}")


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerilaizer


    def post(self, request, *args, **kwargs):
        serializer= RegistrationSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data={
                'email': serializer.validated_data["email"], # type: ignore
            }
            return Response(data=data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Delete the user's token
            request.user.auth_token.delete()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Error logging out.'}, status=status.HTTP_400_BAD_REQUEST)

