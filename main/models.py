from django.db import models


class Passwords(models.Model):
    description = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, unique=True)
    password = models.BinaryField(max_length=150)

    def json(self):
        payload = {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "description": self.description,
        }
        return payload
