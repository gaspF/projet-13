from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileForm
from .models import SavedProfile, Profile
from django.contrib import messages
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db import IntegrityError


class Index(View):
    template_name = 'website/pages/index.html'
    def get(self, request):
        return render(request, self.template_name)


class CreateProfile(View):
    template_name = 'website/pages/createprofile.html'

    @method_decorator(login_required)
    def get(self, request):
        form = ProfileForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                instance = form.customsave(user=request.user)
                profile_id = Profile.objects.get(id=instance.id)
                save = SavedProfile(saved_by=request.user, saved_profile=profile_id)
                save.save()
                messages.success(request, 'Votre profil a bien été créé ! Vous pouvez à présent le consulter.')
            return redirect('profile')


class ProfileList(View):
    model = SavedProfile
    template_name = 'website/pages/profile_list.html'
    paginate_by = 6

    def get(self, request):
        page = request.GET.get('page')
        queryset = SavedProfile.objects.select_related('saved_profile').filter(saved_by=request.user)
        if queryset.count() <= 0:
            return render(request, self.template_name)
        else:
            new_queryset = []
            for list in self.chunks(queryset, 3):
                new_queryset.append(list)

            paginator = Paginator(new_queryset, 10)
            profiles = paginator.get_page(page)
            context_dict = {"queryset" : profiles}
            return render(request, self.template_name, context_dict)

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]


class ProfileSheet(View):
    template_name = 'website/pages/profile_sheet.html'

    def get(self, request, id):
        profile = Profile.objects.get(id=id)
        request.session['profile_id'] = id
        duree_formation = profile.ending_date - profile.starting_date
        context_dict = {'profile': profile,
                        'days': duree_formation.days}
        return render(request, self.template_name, context_dict)


class DeleteProfile(DeleteView):
    """Deleting a post product from user's diary"""
    model = SavedProfile
    template_name = 'website/pages/profile_confirm_delete.html'
    success_url = '/profilelist'
