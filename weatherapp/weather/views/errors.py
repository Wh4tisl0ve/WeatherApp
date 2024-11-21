from django.shortcuts import render


class BadRequestErrorView:
    def __call__(self, request, exception=None):
        return render(request, "weather/layouts/errors/400.html", status=400)


class ForbiddenErrorView:
    def __call__(self, request, exception=None):
        return render(request, "weather/layouts/errors/403.html", status=403)


class NotFoundErrorView:
    def __call__(self, request, exception=None):
        return render(request, "weather/layouts/errors/404.html", status=404)


class ServerErrorView:
    def __call__(self, request, exception=None):
        return render(request, "weather/layouts/errors/500.html", status=500)
