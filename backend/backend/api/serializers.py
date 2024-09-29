from rest_framework import serializers
from .models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'url', 'description', 'timestamp']
        read_only_fields = ['user']