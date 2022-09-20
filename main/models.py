from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.urls import reverse
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField


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
    bio = models.TextField(default='', blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    image = CloudinaryField('image', default='placeholder')
    text = models.TextField(blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    area = models.CharField(max_length=30, null=True, blank=True)
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

    def get_absolute_url(self):
        return reverse("full", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ContactFormMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=80)
    message = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now=True)
    responded = models.BooleanField(choices=((0, "No"), (1, "Yes")), default=0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return (f"from {self.name} | subject: {self.subject}")
