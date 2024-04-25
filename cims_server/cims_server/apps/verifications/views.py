import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from cims_server.utils.utils import verify_key_pair
from .utils import encrypt_payload


class OrdinaryUserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取公钥和私钥
        public_key = request.data.get('public_key')
        private_key = request.data.get('private_key')

        if not public_key or not private_key:
            return Response({"error": "缺少必要的参数"}, status=400)

        if not verify_key_pair(public_key, private_key):
            return Response({"error": "公钥和私钥不匹配"}, status=400)

        payload = encrypt_payload(public_key, private_key)

        # 生成JWT token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token})
