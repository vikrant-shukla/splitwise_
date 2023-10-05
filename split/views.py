from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from split.models import SplitAmount

from .serializers import SplitAmountSerializer, SplitAmountToSerializer


class SplitAPIView(APIView):
    def post(self, request):
        serializer = SplitAmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.split_payment(serializer.validated_data)
        return Response({"status": True})


class MemberPassbook(APIView):
    def post(self, request):
        email = request.data["email"]
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not exists!!!")

        instance = SplitAmount.objects.filter(owe_by__email=email)

        response = {
            "total_balance": instance.aggregate(owe_amount=models.Sum("owe_amount"))[
                "owe_amount"
            ],
            "passbook": SplitAmountToSerializer(instance=instance, many=True).data,
        }

        return Response(response)
