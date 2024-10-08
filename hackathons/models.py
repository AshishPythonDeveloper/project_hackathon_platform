from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserTypeChoices(models.TextChoices):
    ORGANIZER = "ORGANIZER"
    SUBMITTER = "SUBMITTER"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    type = models.CharField(max_length=50, choices=UserTypeChoices.choices)

    def __str__(self):
        return self.user.username


class Hackathon(models.Model):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='background_images/')
    hackathon_image = models.ImageField(upload_to='hackathon_images/')
    submission_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class HackathonRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, related_name='submissions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    summary = models.TextField()
    submission = models.FileField(upload_to='submissions/', blank=True, null=True)
    submission_link = models.URLField(blank=True, null=True)

    def clean(self):
            # Validate based on hackathon's submission type
        if self.hackathon.submission_type == 'image' and not self.submission.name.lower().endswith(
                ('.png', '.jpg', '.jpeg')):
            raise ValidationError('Submission must be an image.')
        elif self.hackathon.submission_type == 'file' and not self.submission.name.lower().endswith(('.zip', '.pdf')):
            raise ValidationError('Submission must be a file.')
        elif self.hackathon.submission_type == 'link' and not self.submission_link:
            raise ValidationError('Submission must be a valid link.')
