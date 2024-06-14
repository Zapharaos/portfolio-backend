from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Portfolio, DefaultUser
from .serializers import PortfolioSerializer


class DefaultPortfolioView(generics.RetrieveAPIView):
    serializer_class = PortfolioSerializer

    def get_object(self):
        default_user_instance = DefaultUser.objects.first()
        if default_user_instance:
            default_user = default_user_instance.user
            return Portfolio.objects.get(idUser=default_user)
        return None

    def get(self, request, *args, **kwargs):
        portfolio = self.get_object()
        if portfolio:
            serializer = self.get_serializer(portfolio)
            return Response(serializer.data)
        return Response({"detail": "Default portfolio not found."}, status=404)
