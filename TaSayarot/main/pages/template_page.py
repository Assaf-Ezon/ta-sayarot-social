from django.contrib.auth.models import User
from django.shortcuts import render
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Users
from abc import abstractmethod, ABC
import json
import os


class MainPage(ABC):
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), "r", encoding='utf-8') as config_file:
        configuration = json.load(config_file)

    HOST = configuration["database"]["HOST"]
    PORT = configuration["database"]["PORT"]
    USERNAME = configuration["database"]["USERNAME"]
    PASSWORD = configuration["database"]["PASSWORD"]
    DATABASE = configuration["database"]["DATABASE"]

    # create a mysql engine
    engine = create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", pool_size=20)

    @abstractmethod
    def view(self, response) -> render:
        pass

    @classmethod
    def _get_online_users(cls) -> dict:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        online_users = {}
        all_users = User.objects.all()

        for user in all_users:
            my_user = session.query(Users).filter_by(name=user.username).first()
            if my_user.status:
                online_users[user.username] = my_user.profile_image

        session.close()
        return online_users

    @classmethod
    def _get_offline_users(cls) -> dict:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        offline_users = {}
        all_users = User.objects.all()

        for user in all_users:
            my_user = session.query(Users).filter_by(name=user.username).first()
            if not my_user.status:
                offline_users[user.username] = my_user.profile_image

        session.close()
        return offline_users

    @classmethod
    def _get_all_users(cls) -> json:
        username_list = [user.username for user in User.objects.all()]
        return json.dumps(username_list)

    @staticmethod
    def erase_everything():
        pass
        # Delete all users
        # User.objects.all().delete()

        # # create django user
        # user = User.objects.create_user(username="אסף איזון", password=sha256("!Assaf15".encode()).hexdigest())
        # user.save()

        # # authenticate user
        # user = authenticate(username="אסף איזון", password=sha256("!Assaf15".encode()).hexdigest())

        # # create sql user
        # Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        # session = Session()  # creates a session
        #
        # new_user = Users(name="אסף איזון",
        #                  email="assafezon@gmail.com",
        #                  role='מש"ק סיירות',
        #                  release_date=datetime(2024, 4, 25),
        #                  profile_image="https://tasayarot.s3.eu-north-1.amazonaws.com/assets/proflie-pages/dafault.jpg",
        #                  password_hash=sha256("!Assaf15".encode()).hexdigest(),
        #                  posts_num=0,
        #                  likes_num=0,
        #                  status=0)
        # session.add(new_user)
        # session.commit()
        #
        # session.close()


# MainPage.erase_everything()
