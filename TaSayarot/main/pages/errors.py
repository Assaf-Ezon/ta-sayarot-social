from django.shortcuts import render
from sqlalchemy.orm import sessionmaker
from .template_page import MainPage
from .models import Users


class Errors(MainPage):
    def view(self, response) -> render:
        pass

    @staticmethod
    def page_not_fount(response) -> render:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session
        account = session.query(Users).filter_by(name=response.user.username).first()
        session.close()
        return render(response, "main/404.html", {"online": Errors._get_online_users(),
                                                  "offline": Errors._get_offline_users(),
                                                  "name": response.user.username,
                                                  "role": account.role,
                                                  "image": account.profile_image,
                                                  "username_list_json": Errors._get_all_users()})

    @staticmethod
    def server_error(response) -> render:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session
        account = session.query(Users).filter_by(name=response.user.username).first()
        session.close()
        return render(response, "main/500.html", {"online": Errors._get_online_users(),
                                                  "offline": Errors._get_offline_users(),
                                                  "name": response.user.username,
                                                  "role": account.role,
                                                  "image": account.profile_image,
                                                  "username_list_json": Errors._get_all_users()})
