from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .models import *
from .views import *
from django.urls import reverse
from users.views import profile
from diary.views import PostsList


class ProfileModelTests(TestCase):
    def test_str(self):
        product = Profile(name="Nom test", objective="marque test")
        self.assertIs(product.__str__(), "Nom test")


class CategoryModelTest(TestCase):
    def test_str(self):
        profile = Profile(name="Test B")
        self.assertIs(profile.__str__(), "Test B")


class ViewsTests(TestCase):

    def setUp(self):
        Profile.objects.create(name='testname', objective='testobjective', hourly_volume="44", forces="testforce", weaknesses="testweak", opportunities='testopport', menaces="testmenaces", offensive="testoffense", defensive="testdefense", preventive="testprevent", emergency="testemergency", step_1="test1", step_1_duration="20", step_2="test2", step_2_duration="21", step_3="test3", step_3_duration="2")
        self.user = User.objects.create(username="Jean", email="jean@yahoo.com", password="machin")
        self.factory = RequestFactory()

    def test_homepage(self):
        response = self.client.get(reverse('apprendre13-index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenue sur Apprendre13")

    def test_user_profile_page_logged_in(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jean@yahoo.com")

    def test_logged_user_profile_page(self):
        request = self.factory.get(reverse('profile-list'))
        request.user = self.user
        response = ProfileList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des projets de Jean")

    def test_create_profile_page(self):
        request = self.factory.get(reverse('create-profile'))
        request.user = self.user
        response = CreateProfile.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nom du projet")


class AnonUser(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnonymousUser()

    def test_anon_user_profile_redirect(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 302)

    def test_anon_user_save_redirect(self):
        request = self.factory.get(reverse('create-profile'))
        request.user = self.user
        response = CreateProfile.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_anon_user_register(self):
        response = self.client.post('/register/')
        self.assertEqual(response.status_code, 200)


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)