from rest_framework import serializers
from server.models import Server, Channel

class ChannelSerializer(serializers.Serializer):
    """
    Serializer for Channel model.
    """
    class Meta:
        """
        Meta class to specify the model and fields.
        """
        model = Channel
        fields = "__all__"  # Serialize all fields of Channel model.

class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for Server model.
    """
    num_members = serializers.SerializerMethodField()  # Custom serializer method field for num_members.
    channel_server = ChannelSerializer(many=True)  # Serialize related Channel instances as a list.

    class Meta:
        """
        Meta class to specify the model, excluded fields, and included fields.
        """
        model = Server
        exclude = ('member',)  # Exclude 'member' field from serialization.
        fields = '__all__'  # Serialize all fields of Server model.

    def get_num_members(self, obj):
        """
        Custom method to retrieve the number of members in a server.
        
        Parameters:
            obj: The Server instance.
        
        Returns:
            The number of members in the server or None if 'num_members' attribute is not present.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Custom method to modify the representation of serialized data.
        
        Parameters:
            instance: The instance of the object being serialized.
        
        Returns:
            Modified representation of serialized data.
        """
        data = super().to_representation(instance)  # Get the default representation.
        num_members = self.context.get("num_members")  # Retrieve num_members from context.
        if not num_members:
            data.pop("num_members", None)  # Remove 'num_members' field if num_members is None.
        return data
