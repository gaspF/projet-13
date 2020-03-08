import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from .forms import PostForm
from website.models import Profile
from django.shortcuts import get_object_or_404
from . import models
from django.core.serializers.json import DjangoJSONEncoder


class PostsList(View):
    template_name = 'pages/posts_list.html'

    def get(self, request):
        id = request.session['profile_id']
        form = PostForm()
        selected_profile = Profile.objects.get(id=id)
        posts = Post.objects.filter(profile=id).filter(author=request.user).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        context_dict = {"posts": posts,
                        "profile": selected_profile,
                        'form': form}

        return render(request, self.template_name, context_dict)


    def post(self, request):
        post_text = request.POST.get('the_post')
        post_subject = request.POST.get('the_subject')
        profile_id = request.session['profile_id']
        selected_profile = Profile.objects.get(id=profile_id)
        response_data = {}
        post = Post(Texte=post_text, Sujet=post_subject, author=request.user, profile=selected_profile, published_date=timezone.now())
        post.save()

        response_data['result'] = 'Entrée postée avec succès'
        response_data['postpk'] = post.pk
        response_data['text'] = post.Texte
        response_data['subject'] = post.Sujet
        response_data['timezone'] = post.published_date

        return JsonResponse(response_data)




class DeletePost(DeleteView):
    """Deleting a post product from user's diary"""
    model = Post
    template_name = 'pages/post_confirm_delete.html'
    success_url = '/diary/list'

