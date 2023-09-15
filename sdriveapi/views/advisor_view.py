"""View module for handling requests about advisor"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sdriveapi.models import Advisor

class AdvisorView(ViewSet):
    """S-Drive Advisor view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single advisor

        Returns:
            Response -- JSON serialized advisor
        """

        advisor = Advisor.objects.get(pk=pk)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all advisors

        Returns:
            Response -- JSON serialized list of advisors
        """

        advisors = Advisor.objects.all()
        serializer = AdvisorSerializer(advisors, many=True)
        return Response(serializer.data)
    
class AdvisorSerializer(serializers.ModelSerializer):
    """JSON serializer for advisor
    """
    class Meta:
        model = Advisor
        fields = ('id', 'full_name', 'experience')