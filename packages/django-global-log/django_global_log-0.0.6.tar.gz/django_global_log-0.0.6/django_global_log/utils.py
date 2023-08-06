from django_global_log.models import DjangoGlobalLog


def get_ip(request):
    if request.META.get("HTTP_X_REAL_IP"):
        return request.META.get("HTTP_X_REAL_IP")
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR").replace(" ", "").split(",")[0]
    return request.META.get("REMOTE_ADDR")


class SaveLogHandler:
    def __init__(self, data):
        self.data = data

    def __call__(self, *args, **kwargs):
        DjangoGlobalLog.objects.create(**self.data)


class GlobalLogExtraFuncMixin:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
