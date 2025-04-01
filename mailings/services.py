from django.core.cache import cache
from django.http import Http404

from config.settings import CACHE_ENABLE

from .models import Mailings


def check_user_permission(user, obj):
    if obj.owner != user and not user.groups.filter(name="Manager").exists():
        raise Http404("У вас нет доступа к этому объекту.")


def get_mailings_from_cache():
    if not CACHE_ENABLE:
        return Mailings.objects.all()
    key = "mailings_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailings.objects.all()
    cache.set(key, mailings)
    return mailings
