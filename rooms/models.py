from django.db import models


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    floor = models.IntegerField()
    total_beds = models.IntegerField(default=1)
    available_beds = models.IntegerField(default=1)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room_image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'
        ordering = ['room_number']

    def __str__(self):
        return f'Room {self.room_number}'

    def save(self, *args, **kwargs):
        if self.available_beds is None:
            self.available_beds = self.total_beds
        if self.available_beds < 0:
            self.available_beds = 0
        if self.available_beds > self.total_beds:
            self.available_beds = self.total_beds
        super().save(*args, **kwargs)
