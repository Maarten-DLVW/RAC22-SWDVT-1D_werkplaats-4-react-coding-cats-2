from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, OpenQSerializer, MultipleChoiceQSerializer
from .models import OpenQ, MultipleChoiceQ
from django.contrib.auth.decorators import login_required


# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Code for the questions inspired by
# https://blog.logrocket.com/using-react-django-create-app-tutorial/
@api_view(['GET', 'POST'])
def open_q_list(request):
    if request.method == 'GET':
        data = OpenQ.objects.all()
        serializer = OpenQSerializer(
            data,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OpenQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def mc_q_list(request):
    if request.method == 'GET':
        data = MultipleChoiceQ.objects.all()
        serializer = MultipleChoiceQSerializer(
            data,
            # context={'request': request},
            many=True
        )
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MultipleChoiceQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def open_q_detail(request, pk):
    try:
        open_q = OpenQ.objects.get(pk=pk)
    except OpenQ.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = OpenQSerializer(open_q,
                                     data=request.data,
                                     context=
                                     {'request': request},
                                     )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def mc_q_detail(request, pk):
    try:
        mc_q = MultipleChoiceQ.objects.get(pk=pk)
    except MultipleChoiceQ.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MultipleChoiceQSerializer(mc_q,
                                               data=request.data,
                                               context=
                                               {'request': request},
                                               )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def hide_open_q(request, pk):
    try:
        open_q_row = OpenQ.objects.get(question_id=pk)
        open_q_row.is_hidden = True
        open_q_row.save()
        return JsonResponse({
            'success': True
        })
    except OpenQ.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Vraag bestaat niet.'
        })


@csrf_exempt
def hide_mc_q(request, pk):
    try:
        mc_q_row = MultipleChoiceQ.objects.get(question_id=pk)
        mc_q_row.is_hidden = True
        mc_q_row.save()
        return JsonResponse({
            'success': True
        })
    except MultipleChoiceQ.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Vraag bestaat niet.'
        })


@csrf_exempt
def edit_open_q(request, pk):
    try:
        open_q_row = OpenQ.objects.get(question_id=pk)
        serializer = OpenQSerializer(open_q_row, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True})
        return JsonResponse({
            'success': False,
            'error': serializer.errors})
    except OpenQ.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Vraag bestaat niet.'
        })
    

@login_required
def current_user(request):
    return JsonResponse({'username': request.user.username})
