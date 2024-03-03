from rest_framework import serializers
from server.models import Category, Server, Channel


class  ChannelSerializer(serializers.Serializer):
    class Meta:
        model = Channel
        firlds = "__all__"
        
class ServerSerializer(serializers.ModelSerializer):
    channel_server = ChannelSerializer(many=True)
    
    class Meta:
        model = Server
        fields = '__all__'
    