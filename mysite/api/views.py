from django.shortcuts import render
from dashboard.models import Recipe, Ingredient
from api.serializers import RecipeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, permissions


# Create your views here.
class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer