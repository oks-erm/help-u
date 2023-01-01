"""
Models of main app.
"""
import random
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.html import mark_safe
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from .managers import CustomUserManager


STATUS = ((0, "Pending"), (1, "Approved"))
ACTIVE = ((0, "Closed"), (1, "Open"))
TYPE = (("receive", "Receive"), ("give", "Give"))
CATEGORIES = (("items", "Items"),
              ("services", "Services"),
              ("support", "Support"))


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
    country = CountryField()
    city = models.CharField(max_length=30, blank=True)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def thumbnail_preview(self):
        if self.userpic:
            # pylint: disable=no-member
            return mark_safe(
                '<img src="{}" width="auto" height="400" />'.format(
                    self.userpic.url))
        return ""


class Post(models.Model):
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="posts", default=22
        )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    image = CloudinaryField('image', default='placeholder')
    text = models.TextField(blank=True)
    country = CountryField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    area = models.CharField(max_length=30, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    relevance = models.IntegerField(choices=ACTIVE, default=1)
    type = models.CharField(choices=TYPE, max_length=10, blank=False)
    category = models.CharField(choices=CATEGORIES, max_length=10, blank=False)
    favourite = models.ManyToManyField(UserProfile, related_name='bookmarks',
                                       blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("main:full", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            draft_slug = str(self.title) + str(random.random())
            # pylint: disable=no-member
            if Post.objects.filter(slug=draft_slug).exists():
                draft_slug = str(self.title) + str(random.random())[::-1]
            self.slug = slugify(draft_slug)

        return super().save(*args, **kwargs)

    @property
    def thumbnail_preview(self):
        if self.image:
            # pylint: disable=no-member
            return mark_safe(
                '<img src="{}" width="auto" height="400" />'.format(
                    self.image.url))
        return ""


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                             related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.user}"


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
        return f"from {self.name} | subject: {self.subject}"


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        # pylint: disable=no-member
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=CustomUser)
