from rest_framework import serializers

class GuidelinesSerializer(serializers.Serializer):
    file = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=1000)
    class Meta:
        fields = ['file', 'content']

class postGuidelinesSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
    class Meta:
        fields = ['content']