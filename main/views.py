from django.shortcuts import render, get_object_or_404,redirect, reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404
from django.core import serializers
from django.utils.decorators import method_decorator 
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
            return redirect('/posts_list/all')

    context = {
        "form": form
    }
    return render(request, "new.html", context)


def post_update(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    form = CreatePostForm(instance=post)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, instance=post)
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
        if self.kwargs.get('type') in ['give', 'receive']:
            posts = qs.filter(type=self.kwargs['type'], status=1)
        else:
            posts = qs.filter(status=1)
        
        query = self.request.GET.get("q")
        if query:
            posts = posts.filter(title__icontains=query)
        
        return posts

    def get(self, request, *args, **kwargs):
        posts = self.get_queryset()
        does_req_accept_json = self.request.accepts("application/json")
        ajax_request = self.request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
        if ajax_request:
            if not posts:
                html = f"There is no '{self.request.GET.get('q')}' in our base, try a different request."
            else:
                html = render_to_string(
                    template_name="posts.html",
                    context={"post_list": posts}
                )
            print(html)

            return JsonResponse({"html_from_view": html}, safe=False)
        else:
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()

            if not allow_empty:
                if self.get_paginate_by(self.object_list) is not None and hasattr(
                    self.object_list, "exists"
                ):
                    is_empty = not self.object_list.exists()
                else:
                    is_empty = not self.object_list
                if is_empty:
                    raise Http404(
                        _("Empty list and “%(class_name)s.allow_empty” is False.")
                        % {
                            "class_name": self.__class__.__name__,
                        }
                    )
            context = self.get_context_data()
            return self.render_to_response(context)

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

