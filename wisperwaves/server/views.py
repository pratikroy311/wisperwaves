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
        try:
            self.check_authentication(request)
            self.filter_by_query_params(request)
            serializer = self.serialize_queryset(request)
            return Response(serializer.data)
        except (ValidationError, AuthenticationFailed) as e:
            return Response({"detail": str(e)}, status=e.status_code)

    def check_authentication(self, request):
        """
        Check authentication for user-specific queries.

        Parameters:
            request: The HTTP request object.

        Raises:
            AuthenticationFailed: If authentication fails.
        """
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed()

    def filter_by_query_params(self, request):
        """
        Filter servers based on query parameters.

        Parameters:
            request: The HTTP request object.
        """
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        if qty:
            self.queryset = self.queryset[:int(qty)]

        if by_server_id:
            self.filter_by_server_id(request, by_server_id)

    def filter_by_server_id(self, request, by_server_id):
        """
        Filter servers by server ID.

        Parameters:
            request: The HTTP request object.
            by_server_id: The server ID to filter by.

        Raises:
            ValidationError: If the server ID is not found or is not valid.
        """
        if not request.user.is_authenticated:
            raise AuthenticationFailed()
        try:
            self.queryset = self.queryset.filter(id=by_server_id)
            if not self.queryset.exists():
                raise ValidationError(detail=f"server id: {by_server_id} not found")
        except ValueError:
            raise ValidationError(detail=f"server id is not valid")

    def serialize_queryset(self, request):
        """
        Serialize the queryset.

        Parameters:
            request: The HTTP request object.

        Returns:
            Serialized server queryset.
        """
        with_num_members = request.query_params.get("with_num_members") == "true"
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return serializer
