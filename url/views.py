from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from url.forms import ResourceForm


class HomeView(FormView):
    template_name = 'home.html'
    form_class = ResourceForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        instance = form.save()

        data = {
            "slug_url": self.request.build_absolute_uri(reverse('share', args=[instance.slug_url])),
            "password": instance.password,
        }
        return self.render_to_response({"data": data})


class ShareView(View):
    pass
