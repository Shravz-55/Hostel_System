from django.db import models
from rooms.models import Room


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    college = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='students/photos/')
    id_proof = models.ImageField(upload_to='students/id_proofs/')
    joining_date = models.DateField()
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_room = None

        if not is_new:
            old_student = Student.objects.filter(pk=self.pk).first()
            if old_student:
                old_room = old_student.room

        super().save(*args, **kwargs)

        if is_new and self.room:
            self.room.available_beds -= 1
            self.room.save()
        elif not is_new:
            if old_room != self.room:
                if old_room:
                    old_room.available_beds += 1
                    old_room.save()
                if self.room:
                    self.room.available_beds -= 1
                    self.room.save()

    def delete(self, *args, **kwargs):
        if self.room:
            self.room.available_beds += 1
            self.room.save()
        super().delete(*args, **kwargs)
