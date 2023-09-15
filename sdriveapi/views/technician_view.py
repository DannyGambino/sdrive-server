"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sdriveapi.models import Technician

class TechnicianView(ViewSet):
    """S-Drive Technician view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        technician = Technician.objects.get(pk=pk)
        serializer = TechnicianSerializer(technician)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        technicians = Technician.objects.all()
        serializer = TechnicianSerializer(technicians, many=True)
        return Response(serializer.data)
    
class TechnicianSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Technician
        fields = ('id', 'full_name', 'specialty')