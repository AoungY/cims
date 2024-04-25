from django.conf import settings
from rest_framework import serializers

from .models import IdentityCard, Passport
from .models import OrdinaryUser


class OrdinaryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdinaryUser
        fields = ['id', 'public_key']


class IdentityCardSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = IdentityCard
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            return settings.MEDIA_STATIC_URL + obj.photo.url
        return None


class PassportSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Passport
        fields = '__all__'

    def get_photo(self, obj):
        if obj.photo:
            return settings.MEDIA_STATIC_URL + obj.photo.url
        return None


class CreateIdentityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityCard
        exclude = ('valid_from', 'valid_to', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'ordinary_user')


class CreatePassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        exclude = ('valid_from', 'valid_to', 'document_number', 'previous_document_number', 'next_document_number', 'another_document_number', 'ordinary_user')
