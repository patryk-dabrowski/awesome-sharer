from django.urls import reverse
from django.views.generic import FormView, DetailView
from django.views.generic.edit import ModelFormMixin

from url.forms import ResourceForm, ShareResourceForm
from url.generator import Generator
from url.models import Resource
from url.signals import update_user_meta


class HomeView(FormView):
    template_name = 'home.html'
    form_class = ResourceForm
    success_url = '/'

    def form_valid(self, form):
        plain_password = Generator.generate(5)

        form.instance.author = self.request.user
        form.instance.set_password(plain_password)
        instance = form.save()

        update_user_meta.send(sender=self.__class__, request=self.request)
        data = {
            "slug_url": self.request.build_absolute_uri(reverse('share', args=[instance.slug_url])),
            "password": plain_password,
        }
        return self.render_to_response({"data": data})


class ShareView(ModelFormMixin, DetailView):
    model = Resource
    template_name = 'share_resource.html'
    slug_url_kwarg = 'slug_url'
    slug_field = 'slug_url'
    form_class = ShareResourceForm
    success_url = '/'

    def get_success_url(self):
        return self.object.redirect_to()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context.update({
            "is_available": self.object.is_available()
        })
        return context

    def form_valid(self, form):
        self.object.increment_visits()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
