"""
Views of the Messenger app.
"""
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class MessagesView(LoginRequiredMixin, generic.TemplateView):
    """
    Renders the Messenger page.
    """
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data (user's first name and id)
        that will be passed to the template when rendering the view.
        """
        return {
                'id': self.request.user.id,
                'name': self.request.user.first_name
            }
