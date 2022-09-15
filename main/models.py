from django.db import models
from django.utils import formats
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField


STATUS = ((0, "Pending"), (1, "Approved"))
ACTIVE = ((0, "Closed"), (1, "Open"))
TYPE = ((0, "Receive"), (1, "Give"))
CATEGORIES = ((0, "Items"), (1, "Services"), (2, "Support"))


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    userpic = CloudinaryField('image', default='placeholder')
    languages = models.CharField(max_length=200)
    bio = models.TextField(default='')
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = CloudinaryField('image', default='placeholder')
    text = models.TextField()
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    relevance = models.IntegerField(choices=ACTIVE, default=1)
    type = models.IntegerField(choices=TYPE)
    category = models.IntegerField(choices=CATEGORIES)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title}"


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
