import pdb
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import ShortenedUrl
from .serializers import UserSerializer


class HomepageView(View):
    template_name = 'pyort/home.html'

    def get(self, request, *args, **kwargs):
        shortenedurl = ShortenedUrl.objects.all().order_by('-id')[:20]
        context = {
            'shortenedurl': shortenedurl
        }
        return render(request, self.template_name, context)


class UserProfileView(View):
    template_name = 'pyort/profile_view.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        # Make sure that the user exists
        try:
            user = User.objects.get(
                username=username,
                is_staff=False,
                is_superuser=False,
                is_active=True
            )
        except User.DoesNotExist:
            raise Http404

        context = {
            'view_user': user,
        }

        return render(request, self.template_name, context)


class UserProfileEditView(View):
    template_name = 'pyort/profile_edit.html'
    context = {}

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        # Check if the person viewing is viewing his/her own profile
        if username != request.user.username:
            raise Http404

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')

        # Check if the person viewing is viewing his/her own profile
        if username != request.user.username:
            raise Http404

        target_url = request.POST.get('target_url')
        if target_url:
            ShortenedUrl.objects.create_short_url(
                user=request.user,
                target_url=target_url
            )

        return render(request, self.template_name, self.context)


class UserListAPIView(ListAPIView):
    """ List all active public users

        Endpoint: /api/v1/users/list
    """
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.model.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True
        )


class UserDetailsAPIView(RetrieveAPIView):
    """ Get active public user details

        Endpoint: /api/v1/users/details/:username
    """
    model = User
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def get_queryset(self):
        qs = self.model.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        if not qs.exists():
            return Response(status.HTTP_404_NOT_FOUND)

        return qs


class ShortenedUrlRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(ShortenedUrl, short_key=kwargs['short_key'])
        self.url = obj.target_url
        return super(ShortenedUrlRedirectView, self).get_redirect_url(*args, **kwargs)
