from django.shortcuts import render
from .pages import Signup, Login, Profile, RandomProfile, Main, Calender, Forum, Admin, Errors


def home(response):
    return Main.view(response)


def calender(response):
    return Calender.view(response)


def forum(response) -> render:
    return Forum.view(response)


def admin(response) -> render:
    return Admin.view(response)


def user_page(response) -> render:
    return Profile.view(response)


def signup(response) -> render:
    return Signup.view(response)


def login(response) -> render:
    return Login.view(response)


def page_not_found(response, exception=None) -> render:
    return Errors.page_not_fount(response)


def server_error(response) -> render:
    return Errors.server_error(response)


def some_account(response, name):
    return RandomProfile.view(response, name)
