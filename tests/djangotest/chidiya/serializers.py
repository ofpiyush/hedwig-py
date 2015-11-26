from rest_framework import serializers
from hedwig.rest_framework.serializers import HedwigModelSerializer
from .models import BasicTest, HiddenTest, ForeignKeyTest, ManyToManyTest
from django.db import models


class BasicTestSerializer(HedwigModelSerializer):
    class Meta:
        model = BasicTest
        fields = (
            'id',
            'char',
            'int',
            'nullable',
            'date',
        )


class HiddenTestSerializer(HedwigModelSerializer):
    class Meta:
        model = HiddenTest
        fields = (
            'id',
            'char',
            'int',
            'nullable',
            'date',
        )


class ForeignKeyTestSerializer(HedwigModelSerializer):
    basic = BasicTestSerializer()

    class Meta:
        model = ForeignKeyTest
        fields = (
            'id',
            'char',
            'int',
            'nullable',
            'date',
            'basic',
        )

    def create(self, validated_data, **kwargs):
        basic_data = validated_data.pop('basic', None)
        if basic_data is None:
            raise serializers.ValidationError("Basic chahiye")
        basic = None
        print basic_data
        if 'id' in basic_data:
            try:
                basic = BasicTest.objects.get(id=basic_data.get('id'))
            except models.ObjectDoesNotExist as e:
                pass
        if basic is None:
            basic_serializer = BasicTestSerializer(data=basic_data)
            basic_serializer.is_valid()
            basic = basic_serializer.save()

        return ForeignKeyTest.objects.create(
            basic=basic,
            char=validated_data.get('char'),
            int=validated_data.get('int'),
            nullable=validated_data.get('nullable'),
            date=validated_data.get('date')
        )


class ManyToManyTestSerializer(serializers.ModelSerializer):
    basic_id = serializers.PrimaryKeyRelatedField(queryset=BasicTest.objects.all())

    class Meta:
        model = ManyToManyTest
        fields = (
            'id',
            'char',
            'int',
            'nullable',
            'date',
            'basic',
            'basic_id'
        )

        depth = 1

    def save(self, **kwargs):
        self.validated_data.pop('basic_id', None)
        return super(ManyToManyTestSerializer, self).save(**kwargs)

