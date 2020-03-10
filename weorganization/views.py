from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from .forms import *
from website.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views.generic import DeleteView
from django.db.models import Sum


class CreateWeekly(FormView):
    """Create a new activity on the weekly sheet"""
    template_name = 'pages/create_weekly_sheet.html'

    @method_decorator(login_required)
    def get(self, request):
        form = DayForm()
        activityform = ActivityForm()
        activitytypeform = ActivityTypeForm()
        return self.render_to_response(self.get_context_data(form=form, activityform=activityform,
                                                             activitytypeform=activitytypeform))

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            activityform = ActivityForm(request.POST, request.FILES)
            activitytypeform = ActivityTypeForm(request.POST, request.FILES)
            form = DayForm(request.POST, request.FILES)
            if form.is_valid() and activitytypeform.is_valid() and activityform.is_valid():
                activity = activityform.save(commit=False)
                activity_type_instance = activitytypeform.save()
                selected_type_activity = ActivityType.objects.get(id=activity_type_instance.id)
                activity.type = selected_type_activity
                activity.save()
                activity_to_day = Activity.objects.get(id=activity.id)
                selected_day = form.save(commit=False)
                selected_day.daily_activity = activity_to_day
                profile_id = request.session['profile_id']
                selected_profile = Profile.objects.get(id=profile_id)
                selected_day.profile = selected_profile
                selected_user = User.objects.get(id=request.user.id)
                selected_day.user = selected_user
                selected_day.save()
                return redirect('create-weekly-sheet')
            else:
                print("Formulaire invalide")
                return redirect('create-weekly-sheet')


class ExistingSheet(View):
    """Displaying an existing sheet with all of the activities saved by the user"""
    template_name = 'pages/existing_sheet.html'

    def get(self, request):
        page = request.GET.get('page')
        profile_id = request.session['profile_id']
        selected_profile = Profile.objects.get(id=profile_id)
        duree_formation = selected_profile.ending_date - selected_profile.starting_date
        monday_set = self.get_query(selected_profile, request.user, 1)
        tuesday_set = self.get_query(selected_profile, request.user, 2)
        wednesday_set = self.get_query(selected_profile, request.user, 3)
        thursday_set = self.get_query(selected_profile, request.user, 4)
        friday_set = self.get_query(selected_profile, request.user, 5)
        saturday_set = self.get_query(selected_profile, request.user, 6)
        sunday_set = self.get_query(selected_profile, request.user, 7)

        monday_queryset = []
        tuesday_queryset = []
        wednesday_queryset = []
        thursday_queryset = []
        friday_queryset = []
        saturday_queryset = []
        sunday_queryset = []


        for list in self.chunks(monday_set, 3):
            monday_queryset.append(list)
        for list in self.chunks(tuesday_set, 3):
            tuesday_queryset.append(list)
        for list in self.chunks(wednesday_set, 3):
            wednesday_queryset.append(list)
        for list in self.chunks(thursday_set, 3):
            thursday_queryset.append(list)
        for list in self.chunks(friday_set, 3):
            friday_queryset.append(list)
        for list in self.chunks(saturday_set, 3):
            saturday_queryset.append(list)
        for list in self.chunks(sunday_set, 3):
            sunday_queryset.append(list)

        monday_paginator = Paginator(monday_queryset, 10)
        new_monday_set = monday_paginator.get_page(page)

        tuesday_paginator = Paginator(tuesday_queryset, 10)
        new_tuesday_set = tuesday_paginator.get_page(page)

        wednesday_paginator = Paginator(wednesday_queryset, 10)
        new_wednesday_set = wednesday_paginator.get_page(page)

        thursday_paginator = Paginator(thursday_queryset, 10)
        new_thursday_set = thursday_paginator.get_page(page)

        friday_paginator = Paginator(friday_queryset, 10)
        new_friday_set = friday_paginator.get_page(page)

        saturday_paginator = Paginator(saturday_queryset, 10)
        new_saturday_set = saturday_paginator.get_page(page)

        sunday_paginator = Paginator(sunday_queryset, 10)
        new_sunday_set = sunday_paginator.get_page(page)


        context_dict = {"monday_set": new_monday_set,
                        "tuesday_set": new_tuesday_set,
                        "wednesday_set": new_wednesday_set,
                        "thursday_set": new_thursday_set,
                        "friday_set": new_friday_set,
                        "saturday_set": new_saturday_set,
                        "sunday_set": new_sunday_set,
                        "profile": selected_profile,
                        "days": duree_formation.days}

        return render(request, self.template_name, context_dict)

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def get_query(profile, user, day_id):
        day_set = Day.objects.filter(profile=profile).filter(user=user).filter(day_name=day_id)
        return day_set


class DeleteActivity(DeleteView):
    """Deleting a post product from user's diary"""
    model = Activity
    template_name = 'pages/activity_confirm_delete.html'
    success_url = '/weekly/existingsheet'