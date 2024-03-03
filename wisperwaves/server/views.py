from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count

class ServerListViewSet(viewsets.ViewSet):
    """
    A viewset for handling server listing operations.
    """
    queryset = Server.objects.all()

    def list(self, request):
        """
        List servers based on various query parameters.

        Parameters:
            request: The HTTP request object.

        Returns:
            HTTP response containing serialized server data.
        """
        # Retrieve query parameters
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Check authentication for user-specific queries
        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Filter servers by category if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter servers by user if requested
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        # Annotate servers with number of members if requested
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        # Limit the number of servers returned if specified
        if qty:
            self.queryset = self.queryset[:int(qty)]

        # Filter servers by server ID if provided
        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"server id: {by_server_id} not found")
            except ValueError:
                raise ValidationError(detail=f"server id is not valid")

        # Serialize the queryset and return response
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
