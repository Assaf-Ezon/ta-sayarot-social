from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from .models import Users, Posts, Comments, Likes
from .template_page import MainPage
import datetime as dt
import json
import boto3


class Calender(MainPage):
    @staticmethod
    @login_required(login_url="/login/")
    def view(response) -> render:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        current_user = session.query(Users).filter_by(name=response.user.username).first()
        posts = {}
        pazamim = ""
        if response.method == "POST":
            if response.POST.get("change-btn"):
                date = datetime.strptime(response.POST.get("change-btn"), "%m/%d/%Y")
                posts = Calender._get_all_posts(date)
                pazamim = Calender._get_close_to_release(date)

            if response.POST.get("submit-comment"):
                Calender._submit_comment(response, current_user)

            if response.POST.get("submit-like"):
                Calender._submit_like(response, current_user)

        session.close()
        return render(response, "main/calender-page.html", {"online": Calender._get_online_users(),
                                                            "offline": Calender._get_offline_users(),
                                                            "name": response.user.username,
                                                            "role": current_user.role,
                                                            "image": current_user.profile_image,
                                                            "username_list_json": Calender._get_all_users(),
                                                            "posts": posts,
                                                            "pazamim": pazamim})

    @classmethod
    def _get_all_posts(cls, date=None) -> list:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        if not date:
            all_posts = session.query(Posts).order_by(desc(Posts.post_id)).all()
        else:
            all_posts = session.query(Posts).filter_by(post_date=date).order_by(
                Posts.post_id.desc()).all()

        posts = []

        for post in all_posts:
            post_user = session.query(Users).filter_by(user_id=post.user_id).first()
            my_file = post.post_file.split(".")

            comments = session.query(Comments).filter_by(post_id=post.post_id).all()
            comment_list = []
            for comment in comments:
                comment_user = session.query(Users).filter_by(user_id=comment.user_id).first()
                text = f"{comment_user.name}: {comment.text}".replace("&#x27;", "")
                comment_list.append(
                    [str(comment_user.profile_image.replace("&#x27;", "")), text.replace("\r\n", "<br>")])

            json_comment_list = json.dumps(comment_list)

            posts.append({
                "post_num": post.post_id,
                "name": f"{post_user.name} - {post_user.role}",
                "date": post.post_date,
                "melel": post.post_text.replace("\r\n", "<br>"),
                "likes": post.likes,
                "file": post.post_file,
                "profile_photo": post_user.profile_image,
                "type": my_file[len(my_file) - 1],
                "comments": json_comment_list
            })

        session.close()
        return posts

    @classmethod
    def _get_close_to_release(cls, date) -> str:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        pazamim = "הקרובים לשחרור: "
        comparison_date = date + timedelta(days=200)
        results = session.query(Users).filter(
            Users.release_date <= comparison_date, Users.release_date >= date).all()

        for result in results:
            pazamim += f" {result.name} ({result.release_date}) "

        session.close()
        return pazamim

    @classmethod
    def _submit_post(cls, response, current_user) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        text = response.POST["melel"]
        file = response.FILES["file"]
        file_path = f"assets/posts/{file.name}"
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_path)

        post = Posts(user_id=current_user.user_id,
                     post_date=dt.date.today(),
                     post_text=text,
                     likes=0,
                     post_file=f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3."
                               f"{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}")
        current_user.posts_num += 1
        session.add(post)
        session.commit()

        session.close()

    @classmethod
    def _submit_comment(cls, response, current_user) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        comment = Comments(user_id=current_user.user_id,
                           post_id=response.POST.get("submit-comment"),
                           text=response.POST["comment"])
        session.add(comment)
        session.commit()

        session.close()

    @classmethod
    def _submit_like(cls, response, current_user) -> None:
        Session = sessionmaker(bind=MainPage.engine)  # creates a session factory
        session = Session()  # creates a session

        if not session.query(Likes).filter_by(user_id=current_user.user_id,
                                              post_id=response.POST.get("submit-like")).first():
            like = Likes(post_id=response.POST.get("submit-like"),
                         user_id=current_user.user_id)
            session.add(like)
            this_post = session.query(Posts).filter_by(
                post_id=response.POST.get("submit-like")).first()
            this_post.likes += 1
            current_user.likes_num += 1
            session.commit()

            session.close()
