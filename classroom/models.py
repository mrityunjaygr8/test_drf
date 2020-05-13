from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def positive_float_validator(val):
    if val < 0:
        raise ValidationError(
            _('%(value)s is negative', params={'value': val})
        )


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    admission_number = models.IntegerField(unique=True)
    is_qualified = models.BooleanField(default=False)
    average_score = models.FloatField(
        blank=True,
        null=True,
        validators=[positive_float_validator]
    )
    username = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        self.username = slugify(self.first_name)
        super(Student, self).save(*args, **kwargs)

    def get_grade(self):
        if 0.0 <= self.average_score < 40.0:
            return "Fail"
        elif 40 <= self.average_score < 70:
            return "Pass"
        elif 70 <= self.average_score <= 100:
            return "Excellent"
        else:
            return "Error"


class Classroom(models.Model):
    name = models.CharField(max_length=120)
    student_capacity = models.IntegerField()
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name
