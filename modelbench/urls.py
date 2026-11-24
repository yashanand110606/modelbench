from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from oauth2_provider.views import AuthorizationView, TokenView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


def root_redirect(request):
    return HttpResponseRedirect("/api/docs/")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("authorize/", AuthorizationView.as_view(), name="authorize"),
    path("token/", TokenView.as_view(), name="token"),
    path("accounts/", include("allauth.urls")),
    path("api/datasets/", include("datasets.urls")),
    path("api/experiments/", include("experiments.urls")),
    path("api/evaluations/", include("evaluations.urls")),
    path("api/benchmarks/", include("benchmarks.urls")),
    path("api/reviews/", include("review_workflow.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
