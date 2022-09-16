from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .models import ContactFormMessage, Post
import os
if os.path.exists('env.py'):
    import env


API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')


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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['key'] = API_KEY
        return context


class PostFull(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)

        maps = "https://www.google.com/maps/embed/v1/place?key="+API_KEY+"&q="+str(post.area)+str(post.city)+","+str(post.country)+"&zoom=13"

        return render(
            request,
            "full.html",
            {
                "post": post,
                "maps": maps,
            },
        )
