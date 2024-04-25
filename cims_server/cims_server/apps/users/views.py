from rest_framework.views import APIView

from cims_server.utils.blockchain.contract import Contract
from users.models import IdentityCard, Passport
from utils.utils import generate_keys
from .serializers import CreateIdentityCardSerializer, CreatePassportSerializer, IdentityCardSerializer, OrdinaryUserSerializer, PassportSerializer

certificate_map = {'0': IdentityCard, '1': Passport}
serializer_map = {'0': IdentityCardSerializer, '1': PassportSerializer}


class UsersView(APIView):
    """
        get->获取所有普通用户的公钥
        post->创建普通用户
    """

    def get(self, request):
        users = OrdinaryUser.objects.all()
        serializer = OrdinaryUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        private_key, public_key = generate_keys()  # 生成公私钥对
        OrdinaryUser.objects.create(private_key=private_key, public_key=public_key)
        return Response({'public_key': public_key}, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    """
    get->获取指定普通用户的私钥
    """

    def get(self, request, pk):
        user = OrdinaryUser.objects.get(id=pk)
        return Response({'private_key': user.private_key})


class UserCertificatesView(APIView):
    """
    get->获取所有拥有身份证/护照的普通用户
    """

    def get(self, request):
        # 从query中获取证书类型
        certificate_type = request.query_params.get('certificate_type', '0')
        try:
            certificate = certificate_map[certificate_type]
        except KeyError:
            return Response("Invalid certificate type", status=status.HTTP_400_BAD_REQUEST)

        certificates = certificate.objects.all()

        # 获取所有拥有身份证/护照的普通用户
        ordinary_users = [c.ordinary_user for c in certificates]
        ordinary_user_serializer = OrdinaryUserSerializer(ordinary_users, many=True)
        return Response(ordinary_user_serializer.data)


class UserSpecificCertificatesView(APIView):
    """
    get->获取指定普通用户的所有身份证/护照
    """

    def get(self, request, pk):
        # 从query中获取证书类型
        certificate_type = request.query_params.get('certificate_type', '0')
        try:
            certificate = certificate_map[certificate_type]
            my_serializer = serializer_map[certificate_type]
        except KeyError:
            return Response("Invalid certificate type", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = OrdinaryUser.objects.get(id=pk)
        except OrdinaryUser.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        certificates = certificate.objects.filter(ordinary_user=user)
        certificate_serializer = my_serializer(certificates, many=True)
        return Response(certificate_serializer.data)


import datetime
import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IdentityCard, OrdinaryUser
from .serializers import IdentityCardSerializer


class AddIdentityCardView(APIView):
    """
    post->为指定用户添加身份证
    """

    def post(self, request, pk):
        try:
            user = OrdinaryUser.objects.get(pk=pk)
        except OrdinaryUser.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateIdentityCardSerializer(data=request.data)
        if serializer.is_valid():
            # 从用户上传的数据中计算证件有效期

            age = datetime.date.today().year - serializer.validated_data["birth_date"].year
            if age < 16:
                duration = 5
            elif age < 25:
                duration = 10
            else:
                duration = 20

            valid_from = datetime.date.today()
            valid_to = valid_from + datetime.timedelta(days=duration * 365)

            data = serializer.validated_data
            data['valid_from'] = valid_from
            data['valid_to'] = valid_to
            data['ordinary_user'] = user

            id_card = IdentityCard.objects.filter(ordinary_user=user).order_by('-valid_from', '-id').first()
            if id_card:
                data['document_number'] = id_card.next_document_number
                data['previous_document_number'] = id_card.document_number
            else:
                # Generate document_number and related fields
                data_to_hash = ','.join([str(data[field.name]) for field in IdentityCard._meta.get_fields() if
                                         field.name not in ['id', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'photo']])
                document_number = hashlib.sha256(data_to_hash.encode()).hexdigest()
                data['document_number'] = document_number
                data['previous_document_number'] = None

            data['next_document_number'] = hashlib.sha256(data['document_number'].encode()).hexdigest()

            another_document = Passport.objects.filter(ordinary_user=user).order_by('-valid_from', '-id').first()
            data['another_document_number'] = another_document.document_number if another_document else None

            new_identity_card = IdentityCard.objects.create(**data)
            return Response(IdentityCardSerializer(new_identity_card).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPassportView(APIView):
    """
    post->为指定用户添加护照
    """

    def post(self, request, pk):
        try:
            user = OrdinaryUser.objects.get(pk=pk)
        except OrdinaryUser.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreatePassportSerializer(data=request.data)
        if serializer.is_valid():
            # 从用户上传的数据中计算证件有效期

            age = datetime.date.today().year - serializer.validated_data["birth_date"].year
            if age < 16:
                duration = 5
            elif age < 25:
                duration = 10
            else:
                duration = 20

            valid_from = datetime.date.today()
            valid_to = valid_from + datetime.timedelta(days=duration * 365)

            data = serializer.validated_data
            data['valid_from'] = valid_from
            data['valid_to'] = valid_to
            data['ordinary_user'] = user

            passport = Passport.objects.filter(ordinary_user=user).order_by('-valid_from', '-id').first()
            if passport:
                data['document_number'] = passport.next_document_number
                data['previous_document_number'] = passport.document_number
            else:
                # Generate document_number and related fields
                data_to_hash = ','.join([str(data[field.name]) for field in Passport._meta.get_fields() if
                                         field.name not in ['id', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'photo']])
                document_number = hashlib.sha256(data_to_hash.encode()).hexdigest()
                data['document_number'] = document_number
                data['previous_document_number'] = None

            data['next_document_number'] = hashlib.sha256(data['document_number'].encode()).hexdigest()

            another_document = IdentityCard.objects.filter(ordinary_user=user).order_by('-valid_from', '-id').first()
            data['another_document_number'] = another_document.document_number if another_document else None

            new_passport_card = Passport.objects.create(**data)
            return Response(PassportSerializer(new_passport_card).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


contract = Contract()
contract.user_public_key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDL1VWTDdoWGFPbU9Eek9hajFBWjNzdzg3bApvTjdRL0FuY0NjajhjQTdUYXUxT2w0amdUQmxSOFZVOEo5dlZkK0liN2NXc2R1UGg1TnNOcXg4NkcxQm5ZRmhXCkt3RnRJeHladjEwS2hrYmtxdm82Nys0cTJ6VzluejdrUVdhaGVEdkpTeFZGdkRxcUJaUjNrWHlQeGcwWW5hMWMKbDF4N0xYSTk4WjltWHFhZ1V3SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQo="
contract.user_private_key = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUNlQUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQW1Jd2dnSmVBZ0VBQW9HQkFMOVJVdnVGZG82WTRQTTUKcVBVQm5lekR6dVdnM3REOENkd0p5UHh3RHROcTdVNlhpT0JNR1ZIeFZUd24yOVYzNGh2dHhheDI0K0hrMncycgpIem9iVUdkZ1dGWXJBVzBqSEptL1hRcUdSdVNxK2pydjdpcmJOYjJmUHVSQlpxRjRPOGxMRlVXOE9xb0ZsSGVSCmZJL0dEUmlkclZ5WFhIc3RjajN4bjJaZXBxQlRBZ01CQUFFQ2dZRUFzOEV0UHJWL1Z5dTg3OHBWUFI1dnkyMk8KajZJK3VBeVhGdTc2c0hSNCtadVZyQ29rcU5uWFVHNTNyeldrRDBXOFpKRmJFVmdEZE5NYUhoV1NHWDVnWTZCbgpuWTRvRmwzT1FZQythZGtlWWJ5Uk1nZ3B4NnNZZk9OTXBvSjFKS1RhSmxqbzRFanlyazFoRlZmRWpZYk5PU0x0ClBkaTV1N3poUElkRW40Ym5MQUVDUVFEcFJwVW1kbHVTaENvRnVhT0k2MndVcVdJK0VmcmlycEt6bXNPUWt0WEQKeDlxRFViSEVsZkdMc0ZoTk1sZHlPSzdseWdXblVha2QzMEpJckFHUkkxREJBa0VBMGZSazVjbXRoME4xOHVsdgp2U3BFbjR6QXhuK2dWY21lNForaFQwdHZSSko4TUJwWS9ZU2d5NE5UTndMc0poWVJZVURVVmRHWVpPNWYrQnFsCkxjNGlFd0pCQUxKZjczTE90Q3p2OUxZV0FtK1RIVDBiWEd6OEVLeS9NcHcxcm03aGFLWGhMenlVL21yRkFVT0EKWDdULzFwQVh1ZDBxUW5KejVlNWFwbk90V3pGaElNRUNRUURSMjhwYWtVc2RVQVgraHV6RWxSSkF0RzBnUEFPawpuRUp1WGFQY1laZFhZR0EzcUs1WXdaQUR2RUdhVkJaOVAwT2lCUzM0bGVjUXcrQXpXMWJOd1NQM0FrQnJ0RmYxCm03cWs5TkZaai9lTm5kMjA5U1UyT0dab0Vrc1JKLzZ3QTByQWFWandOek9tR2VKT3llTjJaZHNWMG94UTVINkwKdWkwK1J1SFl1WkJuMFpMawotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="


class TestView(APIView):
    def get(self, request):
        contract.now_certificate = contract.Passport
        contract.add_data(Passport.objects.first().get_func_param())
        contract.get_data()
        contract.now_certificate = contract.IdentityCard
        contract.get_data()
        contract.add_data(IdentityCard.objects.first().get_func_param())

        return Response("ok", status=status.HTTP_200_OK)
