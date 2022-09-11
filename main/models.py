from django.db import models
from django.utils import formats


class ContactFormMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=80)
    message = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        short_date = 'SHORT_DATETIME_FORMAT'
        return (f"from {self.name} | subject: {self.subject} | "
                f"created: {formats.date_format(self.date, short_date)}")
