from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class MessagesView(LoginRequiredMixin, generic.TemplateView):
    """
    MessagesView is a TemplateView that displays the "messages.html"
    template to the user. The view also adds the user's ID and first
    name to the context data.
    """
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        return {
                'id': self.request.user.id,
                'name': self.request.user.first_name
            }
