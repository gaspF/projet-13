from django import forms
from . models import Profile
from django.forms import formset_factory


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = "Ex: Amélioration du niveau de français"
        self.fields['objective'].initial = "Ex: J'aspire à être capable de m'exprimer à l'écrit au niveau d'un " \
                                           "professionnel de l'édition avant la fin de l'année"
        self.fields['hourly_volume'].initial = 44
        self.fields['forces'].initial = "Vidéo et cours: https://openclassrooms.com/fr/courses/4312781-apprenez-a-appre" \
                                        "ndre/4789871-analysez-vos-forces-et-vos-faiblesses"
        self.fields['weaknesses'].initial = "Voir ci-dessus."
        self.fields['opportunities'].initial = "Vidéo et cours: https://openclassrooms.com/fr/courses/4312781-apprenez-a-apprend" \
                                         "re/4789881-identifiez-vos-opportunites-et-menaces"
        self.fields['menaces'].initial = "Voir ci-dessus"
        self.fields['offensive'].initial = "Vidéo et cours: https://openclassrooms.com/fr/courses/4312781-apprenez-a-apprend" \
                                           "re/4789886-priorisez-vos-differents-projets-detude"
        self.fields['defensive'].initial = "Voir ci-dessus"
        self.fields['preventive'].initial = "Voir ci-dessus"
        self.fields['emergency'].initial = "Voir ci-dessus"
        self.fields['step_1'].initial = "Ex: Rédiger des articles de blog sur des sujets passionnants."
        self.fields['step_2'].initial = "Ex: Faire des dictées."
        self.fields['step_3'].initial = "Ex: Faire des relectures ortho-typographiques."
        self.fields['step_4'].initial = "Ex: Maîtriser toutes les règles de grammaire."
        self.fields['step_5'].initial = "Ex: Lire les oeuvres de membres de l'Académie Française."
        self.fields['step_6'].initial = "Ex: Ecrire au moins 500 mots/jour."
        self.fields['step_1_duration'].initial = 44



    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('day_activity',)

    def customsave(self, user):
        lv = self.save(commit=False)
        lv.created_by = user
        lv.save()
        return lv
