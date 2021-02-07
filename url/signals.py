import django.dispatch

update_user_meta = django.dispatch.Signal(providing_args=['request'])
