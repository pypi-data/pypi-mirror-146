from rest_framework import serializers

from .models import OperationLogEntry


class OperationLogEntrySerializer(serializers.ModelSerializer):
    operator = serializers.CharField(source="user.name", default="", label="操作人")
    show_message = serializers.ListField(child=serializers.CharField(), label="操作内容")
    content_type_name = serializers.CharField(source="content_type.name", label="对象名称")

    class Meta:
        model = OperationLogEntry
        fields = "__all__"
