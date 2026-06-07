from django.db import models
from cloudinary.models import CloudinaryField


class Pastor(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    image = CloudinaryField('image', null=True, blank=True)
    image_word = CloudinaryField('image', null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class PastorWife(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default="Pastor's Wife & Co-Labourer")
    image = CloudinaryField('image', null=True, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "Pastor's Wife"
        verbose_name_plural = "Pastor's Wife"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField('image')
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    image = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class Booking(models.Model):
    CONSULTATION_CHOICES = [
        ('prayer', 'Prayer Session'),
        ('counseling', 'Counseling'),
        ('deliverance', 'Deliverance'),
        ('marriage', 'Marriage Counseling'),
        ('business', 'Business & Financial Breakthrough'),
        ('healing', 'Healing & Health'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_CHOICES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.consultation_type} - {self.preferred_date}'
