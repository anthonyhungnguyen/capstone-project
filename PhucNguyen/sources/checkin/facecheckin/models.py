import uuid
from django.db import models
from django.conf import settings
NUMMER_OF_EMPLOYEE = getattr(settings, 'NUMMER_OF_EMPLOYEE')


class FaceImage(models.Model):
    """
    FaceImage models as facecheckin_faceimage table in database.
    """

    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class Employee(models.Model):
    """
    Employee models as facecheckin_employee table in database.
    """

    id = models.CharField(max_length=20, primary_key=True)
    name = models.TextField()
    dob = models.CharField(max_length=8)
    level = models.IntegerField()
    image = models.ForeignKey(FaceImage, on_delete=models.CASCADE, null=True)
    description = models.TextField(default="")
    activate = models.PositiveIntegerField(default=0)

    # limit number of records
    def save(self, *args, **kwargs):
        objects = Employee.objects.order_by('id')
        if objects.count() == NUMMER_OF_EMPLOYEE:
            objects[0].delete()

        super(Employee, self).save(*args, **kwargs)


class PretrainedImage(models.Model):
    """
    PretrainedImage models as facecheckin_pretrainedimage table in database.
    """

    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class CheckInTime(models.Model):
    """
    CheckInTime models as facecheckin_checkintime table in database.
    """

    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    image = models.ForeignKey(FaceImage, on_delete=models.CASCADE)
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField(null=True)


class Configuration(models.Model):
    """
    Configuration models as facecheckin_configuration table in database.
    """

    key = models.CharField(primary_key=True, max_length=255)
    value = models.CharField(max_length=255)
    default_value = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    edit = models.CharField(max_length=255)
