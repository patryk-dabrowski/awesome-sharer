from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from url.forms import ResourceForm
from url.generator import Generator


class HomeView(FormView):
    template_name = 'home.html'
    form_class = ResourceForm
    success_url = '/'

    def form_valid(self, form):
        plain_password = Generator.generate(5)

        form.instance.author = self.request.user
        form.instance.set_password(plain_password)
        instance = form.save()

        data = {
            "slug_url": self.request.build_absolute_uri(reverse('share', args=[instance.slug_url])),
            "password": plain_password,
        }
        return self.render_to_response({"data": data})


class ShareView(View):
    pass
