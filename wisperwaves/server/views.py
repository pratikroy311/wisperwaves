from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Count

class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    def list(self,request):
        category = request.query_params.get('category')
        qty = request.query_params.get('qty')
        by_user = request.query_params.get("by_user")=="true"
        by_server_id= request.query_params.get("by_server_id")
        
        with_num_members = request.query_params.get("with_num_memebers")== "true"
                
        if by_user or by_server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()
        
        if category:
            self.queryset= self.queryset.filter(category__name=category)
            
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))
        if qty:
            self.queryset= self.queryset[: int(qty)]
        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"server id: {by_server_id} not found")
            except ValueError:
                raise ValidationError(detail=f"server id is not valid")
                          
        serializer = ServerSerializer(self.queryset,many=True,context={"num_members":with_num_members})
        return Response(serializer.data)
            