from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class SingletonUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.first()

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        return Response({"detail": "User not found."}, status=404)
