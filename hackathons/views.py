from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from .models import Hackathon, Submission, HackathonRegistration
from .permissions import OrganizerUserPermission
from .serializers import HackathonSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [OrganizerUserPermission]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        hackathon = self.get_object()
        registration, created = HackathonRegistration.objects.get_or_create(user=request.user, hackathon=hackathon)

        if created:
            return Response({'status': 'registered'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already registered'}, status=status.HTTP_200_OK)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
