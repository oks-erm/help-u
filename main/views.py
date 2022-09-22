from django.shortcuts import render, get_object_or_404,redirect, reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cloudinary.forms import cl_init_js_callbacks      
from .models import ContactFormMessage, Post
from .forms import CreatePostForm
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


def post_create(request):
    form = CreatePostForm()
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('/posts/1')

    context = {
        "form": form
    }
    return render(request, "new.html", context)


def post_update(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    form = CreatePostForm(instance=post)
    if request.method == "POST":
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('full', kwargs={'slug': slug}))

    context = {
        "form": form,
        "post": post
    }
    return render(request, "update.html", context)


@method_decorator(login_required, name='dispatch')
class PostList(generic.ListView):
    model = Post
    template_name = "posts_list.html"
    paginate_by = 12

    def get_queryset(self):
        qs = super(PostList, self).get_queryset()
        if self.kwargs.get('type') in ['0', '1']:
            qs = qs.filter(type=self.kwargs['type'], status=1)
        return qs.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = API_KEY
        return context


@method_decorator(login_required, name='dispatch')
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


