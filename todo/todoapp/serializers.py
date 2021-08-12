import datetime

from rest_framework import serializers
from .models import RegisteredUsers, Todo


class CreateTodoSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)

    def create(self, validated_data):
        # import ipdb;ipdb.set_trace()
        validated_data["user_id"] = self.context["request"].user.id
        instance = Todo.objects.create(**validated_data)
        return instance


class UpdateTodoSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    detail = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.title = validated_data["title"]
        instance.detail = validated_data["detail"]
        instance.modified_date = datetime.datetime.now()

        instance.save()

        return instance

