from django.shortcuts import render
from django.views import generic
from .models import ContactFormMessage, Post


def home_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')

        new = ContactFormMessage(
            name=name,
            email=email,
            subject=subject,
            message=msg,
            )
        new.save()

    return render(request, 'index.html')


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "posts_list.html"
    paginate_by = 10


# def posts_list(request):
#     posts = Post.objects.all()
#     context = {
#         'posts': posts
#     }
#     return render(request, 'posts_list.html', context)
