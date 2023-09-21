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
            service_tickets = ServiceTicket.objects.filter(technician__user=request.auth.user)

        serialized = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_ticket = ServiceTicket()
        new_ticket.advisor = Advisor.objects.get(user=request.auth.user)
        new_ticket.description = request.data['description']
        new_ticket.vehicle = request.data['vehicle']
        new_ticket.customer = request.data['customer']
        new_ticket.ro_identifier = request.data['ro_identifier']

        new_ticket.save()

        serialized = ServiceTicketSerializer(new_ticket, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests"""

        ticket = ServiceTicket.objects.get(pk=pk)

        technician_id = request.data['technician']
        
        if isinstance(technician_id, int):
            assigned_technician = Technician.objects.get(pk=technician_id)

            ticket.technician = assigned_technician
        else:            
            ticket.advisor = Advisor.objects.get(user=request.auth.user)
            ticket.description = request.data['description']
            ticket.vehicle = request.data['vehicle']
            ticket.customer = request.data['customer']
            ticket.date_completed = request.data['date_completed']

        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests"""

        service_ticket = ServiceTicket.objects.get(pk=pk)
        service_ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
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
        fields = ('id', 'ro_identifier', 'advisor', 'customer', 'technician', 'vehicle', 'description', 'date_completed')
        depth = 1