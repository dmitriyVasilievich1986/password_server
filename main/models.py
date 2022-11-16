from django.db import models


class Field(models.Model):
    value = models.BinaryField(max_length=150)
    name = models.CharField(max_length=150)

    password = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name="fields",
        to="Passwords",
    )


class Passwords(models.Model):
    description = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "fields": {x.name: x.value for x in self.fields.all()},
        }
