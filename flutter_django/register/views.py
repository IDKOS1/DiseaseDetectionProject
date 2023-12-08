from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework import exceptions, status
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, ImageUpload

import os

from .serializers import ImageUploadSerializer


class NotFoundException(APIException):
    status_code = 400
    default_detail = 'request를 다시 확인해주세요'
    default_code = 'KeyNotFound'


@api_view(['POST'])
def SignupView(request):
    if not ('email' and 'password' in request.data):
        raise NotFoundException()

    if User.objects.filter(email=request.data['email']).exists():
        return HttpResponseBadRequest("이미 존재하는 이메일 입니다.")
    else:
        user = User.objects.create_user(email=request.data['email'], password=request.data['password'],
                                        username=request.data['username'], birth=request.data['birth'],
                                        gender=request.data['gender'], number=request.data['number'],
                                        farm=request.data['farm'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({"Token": token.key})


@api_view(['POST'])
def LoginView(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(username=email, password=password)

    if user is not None:
        token = Token.objects.get(user=user)
        # User 객체를 찾았으므로 User의 id를 반환
        user_id = user.id
        return Response({"token": token.key, "id": user_id, "name": user.username, "farm": user.farm, "email": user.email}, content_type=u"application/json; charset=utf-8")

    else:
        try:
            # 이메일로 사용자를 찾았지만 비밀번호가 틀린 경우
            user = User.objects.get(email=email)
            return Response({"message": "비밀번호가 틀립니다."}, content_type=u"application/json; charset=utf-8", status=401)
        except User.DoesNotExist:
            # 이메일로 사용자를 찾지 못한 경우
            return Response({"message": "존재하지 않는 이메일 입니다."}, content_type=u"application/json; charset=utf-8",
                            status=401)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkToken(request):
    try:
        return Response({"message": "인증 완료"}, content_type=u"application/json; charset=utf-8")
    except TokenAuthentication.DoesNotExist:
        return Response({"message": "만료된 계정 입니다."}, content_type=u"application/json; charset=utf-8", status=status.HTTP_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def imagesUpload(request):
    try:
        today = timezone.now().strftime('%y%m%d')
        user = request.user
        root = 'C:/Users/Hoseo/Desktop/project/images'
        counter = 0
        DIRECTORY = f'{root}/{user}/{today}_{counter:02d}'  # 저장 위치 지정

        # 중복된 경로가 있으면 새로운 이름의 폴더 생성
        if os.path.exists(DIRECTORY):
            while True:
                counter += 1
                new_directory = f'{root}/{user}/{today}_{counter:02d}'
                if not os.path.exists(new_directory):
                    DIRECTORY = new_directory
                    print(f'New Directory: {DIRECTORY}')
                    os.makedirs(DIRECTORY, exist_ok=True)
                    break
        else:
            print(f'New Directory: {DIRECTORY}')
            os.makedirs(DIRECTORY, exist_ok=True)


        # 17장의  이미지를 서로 다른 이름 으로 저장
        for i in range(17):
            file_name = f'image_{i}'  # 파일 필드 이름
            uploaded_file = request.FILES.get(file_name)
            if uploaded_file:
                file_path = os.path.join(DIRECTORY, f'image_{i}.jpg')  # 파일 경로 설정
                print(f'uploaded image_{i}')
                # 파일 저장
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

        print('upload done')

        # DB에 정보 저장
        db_image = ImageUpload(location=DIRECTORY, upload_user=user, number_images=len(request.FILES))
        db_image.save()
        return Response("업로드 되었습니다.", content_type=u"application/json; charset=utf-8")

    except BaseException:
        return Response("업로드 실패",content_type=u"application/json; charset=utf-8", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def loadResult(request):
    try:
        user = request.user
        user_id = user.id
        print(f"user id={user_id}")
        results = ImageUpload.objects.filter(upload_user=user_id)
        print(results.count())


        if results.exists():
            data = [{"location": result.location,
                     "upload_date": result.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                     "number_images": result.number_images, "is_done": result.is_done, "Edwardsiella": result.Edwardsiella,
                     "Vibrio": result.Vibrio, "Streptococcus": result.Streptococcus, "Tenacibaculumn": result.Tenacibaculumn,
                     "Enteromyxum": result.Enteromyxum, "Miamiensis": result.Miamiensis, "VHSV": result.VHSV
                     } for result in results]
            print(data)

            return JsonResponse(data, safe=False)
        else:
            # Handle the case where no results are found for the user
            response_data = {"length": 0}
            return Response(response_data)
    except Exception as e:
        # Handle exceptions gracefully, e.g., log the error
        print(f"Error in loadResult: {str(e)}")
        return Response({"error": "An error occurred"}, status=500)
