from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cims_server.utils.blockchain.contract import Contract
from users.models import IdentityCard,Passport

contract = Contract()
contract.user_public_key = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDL1VWTDdoWGFPbU9Eek9hajFBWjNzdzg3bApvTjdRL0FuY0NjajhjQTdUYXUxT2w0amdUQmxSOFZVOEo5dlZkK0liN2NXc2R1UGg1TnNOcXg4NkcxQm5ZRmhXCkt3RnRJeHladjEwS2hrYmtxdm82Nys0cTJ6VzluejdrUVdhaGVEdkpTeFZGdkRxcUJaUjNrWHlQeGcwWW5hMWMKbDF4N0xYSTk4WjltWHFhZ1V3SURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQo="


class TestView(APIView):

    def get(self, request):
        contract.now_certificate = contract.Passport
        contract.add_data(Passport.objects.first().get_func_param())
        contract.get_data()
        contract.now_certificate = contract.IdentityCard
        contract.get_data()
        contract.add_data(IdentityCard.objects.first().get_func_param())

        return Response("ok", status=status.HTTP_200_OK)
