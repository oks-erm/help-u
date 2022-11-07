from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.template.loader import render_to_string
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ContactFormMessage, Post, Comment
from messenger.models import Message
from .forms import CreatePostForm
from .serialisers import CustomUserSerializer
import os
if os.path.exists('env.py'):
    import env


API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')


class LandingView(generic.TemplateView):
    template_name = "index.html"

    def post(self, request):
        new = ContactFormMessage(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
            )
        new.save()
        return HttpResponse("")


class PostList(LoginRequiredMixin, generic.ListView):
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


class PostFull(LoginRequiredMixin, generic.DetailView):
    template_name = "full.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(status=1)
        return queryset
    
    def post(self, request, slug, *args, **kwargs):

        new = Comment(
            post=self.get_object(),
            user=request.user.userprofile,
            body=request.POST.get('body'),
            )
        new.save()
        return HttpResponse("")

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(approved=True, post=self.object.id)
        context = super().get_context_data(**kwargs)
        context['key'] = API_KEY
        context['comments'] = comments
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "new.html"
    form_class = CreatePostForm

    def get_success_url(self):
        return reverse('main:posts_list', kwargs={'type': self.object.type})

    def form_valid(self, form):
        form.instance.author = self.request.user.userprofile
        form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "update.html"
    form_class = CreatePostForm
    queryset = Post.objects.filter(status=1)

    def get_success_url(self):
        return reverse('main:full', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.save()
        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "delete.html"
    queryset = Post.objects.filter(status=1)

    def get_success_url(self):
        return reverse('main:posts_list', kwargs={'type': self.object.type})


class BookMark(generic.View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.favourite.filter(id=request.user.id).exists():
            post.favourite.remove(request.user.userprofile.id)
        else:
            post.favourite.add(request.user.userprofile.id)

        return HttpResponse("",)


def messages(request):
    unread_count = Message.objects.filter(to_user=request.user, read=False).count()
    context = {'unread': unread_count}
    return JsonResponse(context)
