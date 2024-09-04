from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Hackathon, Submission
from .permissions import OrganizerUserPermission
from .serializers import HackathonSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer
    permission_classes = [OrganizerUserPermission]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
