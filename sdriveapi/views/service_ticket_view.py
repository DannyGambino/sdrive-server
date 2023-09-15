"""View module for handling requests about service ticket"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from sdriveapi.models import ServiceTicket, Advisor, Technician

class ServiceTicketView(ViewSet):
    """S-Drive ServiceTicket view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single service ticket

        Returns:
            Response -- JSON serialized service ticket
        """
        serviceTicket = ServiceTicket.objects.get(pk=pk)
        serializer = ServiceTicketSerializer(serviceTicket)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all service tickets

        Returns:
            Response -- JSON serialized list of service tickets
        """
        service_tickets = []
        
        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    service_tickets = service_tickets.filter(date_completed__isnull=False)

                if request.query_params['status'] == "all":
                    pass

        else:
            service_tickets = ServiceTicket.objects.filter(customer__user=request.auth.user)

        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class TicketAdvisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        fields = ('id', 'user', 'experience')

class TicketTechnicianSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technician
        fields = ('id', 'user', 'specialty')

class ServiceTicketSerializer(serializers.ModelSerializer):

    advisor = TicketAdvisorSerializer(many=False)
    technician = TicketTechnicianSerializer(many=False)

    class Meta:
        model = ServiceTicket
        fields = ('id', 'advisor', 'technician', 'customer', 'vehicle', 'description', 'date_completed')
        depth = 1