from rest_framework import serializers

from .models import IdentityCard, Passport
from .models import OrdinaryUser


class OrdinaryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinaryUser
        fields = ['id', 'public_key']


class IdentityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityCard
        fields = '__all__'


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'


class CreateIdentityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityCard
        exclude = ('valid_from', 'valid_to', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'ordinary_user')


class CreatePassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        exclude = ('valid_from', 'valid_to', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'ordinary_user')
