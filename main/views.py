# pylint: disable=attribute-defined-outside-init
"""
Views of main app.
"""
import gettext
from django.shortcuts import get_object_or_404, reverse
from django.views import generic
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import ContactFormMessage, Post, Comment
from .forms import CreatePostForm
# pylint: disable=wrong-import-order
import os
if os.path.exists('env.py'):
    import env  # noqa # pylint: disable=unused-import


_ = gettext.gettext
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')


class LandingView(generic.TemplateView):
    """
    A view for displaying the Home page.
    """
    template_name = "index.html"

    def post(self, request):
        """
        Handles post requests to create new contact form messages.
        """
        new = ContactFormMessage(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
            )
        new.save()
        return HttpResponse("")


class PostList(LoginRequiredMixin, generic.ListView):
    """
    A view for displaying a list of posts.
    """
    model = Post
    template_name = "posts_list.html"
    paginate_by = 12

    def get_queryset(self):
        """
        Filter queryset by post type and the query parameter.
        """
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
        """
        Handles both regular and ajax requests for the posts page.
        For regular requests, it renders the 'posts.html' template with the
        context data of the paginated queryset.
        For ajax requests, it renders the same template but returns the
        rendered html in a JsonResponse.
        """
        posts = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
                posts, 12
            )
        # check if the request is an ajax request that accepts json
        does_req_accept_json = self.request.accepts("application/json")
        ajax_request = (self.request.headers.get("x-requested-with")
                        == "XMLHttpRequest" and does_req_accept_json)
        if ajax_request:
            # render the template with the paginated queryset and
            # and return the rendered html in a JsonResponse.
            if not posts:
                html = (f"There is no '{self.request.GET.get('q')}'"
                        "in our base, try a different request.")
            else:
                html = render_to_string(
                    template_name="posts.html",
                    context={
                        'post_list': queryset,
                        "paginator": paginator,
                        "page_obj": page,
                        "is_paginated": is_paginated,
                        "key": API_KEY
                        }
                    )
            return JsonResponse({"html_from_view": html}, safe=False)
        else:
            # regular request
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data (API_KEY for Google Maps)
        that will be passed to the template when rendering the view.
        """
        context = super().get_context_data(**kwargs)
        context['key'] = API_KEY
        return context


class PostFull(LoginRequiredMixin, generic.DetailView):
    """
    A view for displaying a post in details.
    """
    template_name = "full.html"
    context_object_name = "post"

    def get_queryset(self):
        """
        Filter queryset by status to show
        only approved posts.
        """
        # pylint: disable=no-member
        queryset = Post.objects.filter(status=1)
        return queryset

    # The method uses the self.get_object() method which is a built
    # in method from the singleObjectMixin to get the post and if
    # not passed **kwargs it will raise an error.
    # pylint: disable=unused-argument
    def post(self, request, **kwargs):
        """
        Handles post requests to create new comment.
        """
        new = Comment(
            post=self.get_object(),
            user=request.user.userprofile,
            body=request.POST.get('body'),
            )
        new.save()
        return HttpResponse("")

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data (API_KEY for Google Maps and comments)
        that will be passed to the template when rendering the view.
        """
        # pylint: disable=no-member
        comments = Comment.objects.filter(approved=True, post=self.object.id)
        context = super().get_context_data(**kwargs)
        context['key'] = API_KEY
        context['comments'] = comments
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin,
                     generic.CreateView):
    """
    A view for creating a new post.
    """
    template_name = "new.html"
    form_class = CreatePostForm
    success_message = "Your post will be published after moderation"

    def get_success_url(self):
        """
        Returns the url to redirect to after successful post creation.
        """
        return reverse('main:posts_list', kwargs={'type': self.object.type})

    def form_valid(self, form):
        """
        Handles the form validation and post creation.
        """
        form.instance.author = self.request.user.userprofile
        form.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    A view for updating a post.
    """
    template_name = "update.html"
    form_class = CreatePostForm
    queryset = Post.objects.filter(status=1)  # pylint: disable=no-member

    def get_success_url(self):
        """
        Returns the url to redirect to after successful post updating.
        """
        return reverse('main:full', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        """
        Handles the form validation and updating a post.
        """
        form.save()
        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    A view for deleting a post.
    """
    template_name = "delete.html"
    queryset = Post.objects.filter(status=1)  # pylint: disable=no-member

    def get_success_url(self):
        """
        Returns the url to redirect to after successful post deletion.
        """
        return reverse('main:posts_list', kwargs={'type': self.object.type})


class BookMark(generic.View):
    """
    A view for bookmarking a post.
    """
    def post(self, request, slug):
        """
        If the current user has already bookmarked the post, it removes
        the user's bookmark. If the user has not bookmarked the post,
        it adds the user's bookmark.
        """
        post = get_object_or_404(Post, slug=slug)
        if post.favourite.filter(id=request.user.userprofile.id).exists():
            post.favourite.remove(request.user.userprofile.id)
        else:
            post.favourite.add(request.user.userprofile.id)

        return HttpResponse("",)
