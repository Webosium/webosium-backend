from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status,viewsets

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from rest_framework.authtoken.models import Token
from rest_framework import permissions
from core.permissions import IsOwner, IsOwnerOrAdmin, ActionBasedPermission

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from core.serializers import *
from core.models import *

from django.http import HttpResponse

def index(request):
    return HttpResponse('OK')

class UserCreateAPIView(viewsets.ModelViewSet):
    queryset           = User.objects.all()
    serializer_class   = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserInfoAPIView(viewsets.ReadOnlyModelViewSet):
    model              = User
    serializer_class   = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class EventAllApiViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = EventSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        title = self.request.query_params.get('title')

        if tags is None and title is None:
            return Event.objects.all()\
                .filter(archived=False)\
                .order_by('-date')\
                .filter(status='A')
        elif tags is None:
            return Event.objects.all()\
                .filter(name__icontains=title)\
                .filter(status='A')\
                .filter(archived=False)\
                .order_by('-date')\
                .distinct()
        elif title is None:
            return Event.objects.all()\
                .filter(tags__name__in=tags.split(','))\
                .filter(status='A')\
                .filter(archived=False)\
                .order_by('-date')\
                .distinct()
        else:
            return Event.objects.all()\
                .filter(tags__name__in=tags.split(','))\
                .filter(name__icontains=title)\
                .filter(status='A')\
                .filter(archived=False)\
                .order_by('-date')\
                .distinct()


class EventUserApiViewSet(viewsets.ModelViewSet):
    serializer_class   = EventSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)
    http_method_names  = ['get']

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status=='all':
            return Event.objects.all()\
                .filter(created_by=self.request.user, archived=False)
        elif status=='pending':
            return Event.objects.all()\
                .filter(created_by=self.request.user)\
                .filter(status='P')\
                .filter(archived=False)\
                .distinct()
        elif status=='approved':
            return Event.objects.all()\
                .filter(created_by=self.request.user)\
                .filter(status='A')\
                .filter(archived=False)\
                .distinct()
        elif status=='rejected':
            return Event.objects.all()\
                .filter(created_by=self.request.user)\
                .filter(status='R')\
                .filter(archived=False)\
                .distinct()
        else:
            return Event.objects.all()\
                .filter(created_by=self.request.user, archived=False)


class EventApiViewSet(viewsets.ModelViewSet):
    serializer_class   = EventEditSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope, IsOwnerOrAdmin)

    def get_queryset(self):
        return Event.objects.all().filter(archived=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({"detail": "Cannot find event"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"detail": "event has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

class TagAllApiViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = TagSerializer

    def get_queryset(self):
        return Tag.objects.all().filter(archived=False)


class TagApiViewSet(viewsets.ModelViewSet):
    serializer_class   = TagSerializer
    permission_classes = (permissions.IsAuthenticated, TokenHasReadWriteScope,)

    def get_queryset(self):
        return Tag.objects.all().filter(archived=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)