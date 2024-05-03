import datetime
import hashlib

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cims_server.utils.blockchain.contract import Contract
from cims_server.utils.pagination import StandardResultsSetPagination
from cims_server.utils.utils import generate_keys
from users.models import Passport
from verifications.utils import JWTAuthentication, get_payload
from .models import IdentityCard, OrdinaryUser
from .serializers import CreateIdentityCardSerializer, CreatePassportSerializer, OrdinaryUserSerializer, PassportSerializer
from .serializers import IdentityCardSerializer

certificate_map = {'0': IdentityCard, '1': Passport}
serializer_map = {'0': IdentityCardSerializer, '1': PassportSerializer}
contract = Contract()


class UsersView(APIView):
    """
        get->获取所有普通用户的公钥
        post->创建普通用户
    """
    # 设置分页
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        users = OrdinaryUser.objects.all().order_by('-id')

        # 分页处理
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request, view=self)

        if page is not None:
            serializer = OrdinaryUserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response("No pages", status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        private_key, public_key = generate_keys()  # 生成公私钥对
        OrdinaryUser.objects.create(private_key=private_key, public_key=public_key)

        return Response({'public_key': public_key, 'private_key': private_key}, status=status.HTTP_201_CREATED)


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
    pagination_class = StandardResultsSetPagination

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
        # 去重
        ordinary_users = list(set(ordinary_users))
        # ordinary_users根据id排降序
        ordinary_users.sort(key=lambda x: x.id, reverse=True)

        # 分页处理
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(ordinary_users, request, view=self)

        if page is not None:
            ordinary_user_serializer = OrdinaryUserSerializer(page, many=True)
            return paginator.get_paginated_response(ordinary_user_serializer.data)
        else:
            return Response("No pages", status=status.HTTP_204_NO_CONTENT)


class UserSpecificCertificatesView(APIView):
    """
    get->获取指定普通用户的所有身份证/护照
    """
    pagination_class = StandardResultsSetPagination

    def get(self, request, pk):
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

        certificates = certificate.objects.filter(ordinary_user=user).order_by('-valid_from', '-id')

        # 分页处理
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(certificates, request, view=self)

        if page is not None:
            certificate_serializer = my_serializer(page, many=True)
            return paginator.get_paginated_response(certificate_serializer.data)
        else:
            return Response("No pages", status=status.HTTP_204_NO_CONTENT)


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
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

        identity_card = IdentityCard.objects.create(**data)
        # 将数据上传到区块链
        try:
            contract.user_public_key = user.public_key
            contract.now_certificate = contract.IdentityCard
            contract.add_data(identity_card.get_func_param())
        except:
            # 如果上传到区块链失败，删除数据库中的数据
            identity_card.delete()
            return Response("Failed to upload data to blockchain", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(IdentityCardSerializer(identity_card).data, status=status.HTTP_201_CREATED)


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
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        # 创建Passport对象，但不立即保存到数据库
        passport = Passport.objects.create(**data)
        # 将数据上传到区块链
        try:
            contract.user_public_key = user.public_key
            contract.now_certificate = contract.Passport
            contract.add_data(passport.get_func_param())
        except:
            # 如果上传到区块链失败，删除数据库中的数据
            passport.delete()
            return Response("Failed to upload data to blockchain", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(PassportSerializer(passport).data, status=status.HTTP_201_CREATED)


def get_certificates(request):
    """
        从request中获取用户想要的证书类型，解密用户信息，获取用户的公钥和私钥
        最终从区块链中获取用户的证书数据
    """
    # 从query中获取证书类型
    certificate_type = request.query_params.get('certificate_type', '0')
    if certificate_type == '0':
        contract.now_certificate = contract.IdentityCard
        Certificate = IdentityCard
        Certificate_serializer = IdentityCardSerializer
    else:
        contract.now_certificate = contract.Passport
        Certificate = Passport
        Certificate_serializer = PassportSerializer

    # 获取request中的'Authorization'，并解密后获取用户私钥
    decrypted_payload = get_payload(request)
    if decrypted_payload is None:
        return Response({"error": "无法解密用户信息"}, status=status.HTTP_400_BAD_REQUEST)

    contract.user_private_key = decrypted_payload['private_key']
    contract.user_public_key = decrypted_payload['public_key']
    data = contract.get_data()

    # 将数据解析为IdentityCard对象
    certificates = [Certificate.create_from_list(i) for i in data]

    # .order_by('-valid_from', '-id')表示按照valid_from降序和id降序排列
    certificates.sort(key=lambda x: (x.valid_from, x.id), reverse=True)
    return certificates, Certificate, Certificate_serializer


class CertificatesView(APIView):
    """
    get->获取用户的所有证书
    """
    # 需要登录
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    pagination_class = StandardResultsSetPagination  # 设置分页

    def get(self, request):
        certificates, Certificate, Certificate_serializer = get_certificates(request)
        # 分页处理
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(certificates, request, view=self)

        if page is not None:
            certificate_serializer = Certificate_serializer(page, many=True)
            return paginator.get_paginated_response(certificate_serializer.data)
        else:
            return Response("No pages", status=status.HTTP_204_NO_CONTENT)


class CertificatesLatestView(APIView):
    """
    get->获取用户最新的证书
    """
    # 需要登录
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificates, Certificate, Certificate_serializer = get_certificates(request)

        if not certificates:
            return Response("No certificates", status=status.HTTP_204_NO_CONTENT)
        # 获取最新的证书，即certificates中valid_to最大的证书
        latest_certificate = max(certificates, key=lambda x: (x.valid_to, x.id))
        return Response(Certificate_serializer(latest_certificate).data)
