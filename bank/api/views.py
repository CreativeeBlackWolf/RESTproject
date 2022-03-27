# from django.forms import model_to_dict
# from django.shortcuts import render
# from rest_framework.response import Response
# from .models import *
from rest_framework import generics, viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import *


# Create your views here.
class UsersAPIViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

