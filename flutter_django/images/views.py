from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils import timezone
from django.http import HttpResponseBadRequest
from rest_framework.exceptions import APIException
from rest_framework import exceptions, status
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate


@api_view(['POST'])
def imagesUploa(request):
    user_id = request.user.id
    upload_date = timezone.now()
    return Response({"message": "이미지 경로입니다."});


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def imagesUpload(request):
    try:
        return Response("인증 완료")
    except TokenAuthentication.DoesNotExist:
        return HttpResponseBadRequest("만료된 계정입니다.")
