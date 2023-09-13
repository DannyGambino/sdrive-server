from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from sdriveapi.models import Advisor
from sdriveapi.models import Technician

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
    request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(email=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    account_type = request.data.get('account_type', None)
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)

    if account_type is not None \
        and email is not None\
        and first_name is not None \
        and last_name is not None \
        and password is not None:

        if account_type == 'advisor':
            experience = request.data.get('experience', None)
            if experience is None:
                return Response(
                    {'message': 'You must provide an experience for a advisor'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif account_type == 'technician':
            specialty = request.data.get('specialty', None)
            if specialty is None:
                return Response(
                    {'message': 'You must provide a specialty for an technician'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'message': 'Invalid account type. Valid values are \'advisor\' or \'technician\''},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )
        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account = None

        if account_type == 'advisor':
            account = Advisor.objects.create(
                experience=request.data['experience'],
                user=new_user
            )
        elif account_type == 'technician':
            new_user.is_staff = True
            new_user.save()

            account = Technician.objects.create(
                specialty=request.data['specialty'],
                user=new_user
            )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=account.user)
        # Return the token to the client
        data = { 'token': token.key }
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, last_name and account_type'}, status=status.HTTP_400_BAD_REQUEST)