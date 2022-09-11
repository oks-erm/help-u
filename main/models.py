from django.db import models


class ContactFormInquiry(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=80)
    message = models.CharField(max_length=2000)

    def __str__(self):
        return f"Inquiry from {self.name}, subject: {self.subject}"
