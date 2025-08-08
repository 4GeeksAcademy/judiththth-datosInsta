from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=True)
    lastname: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #-------------------RELACIONES-------------------------------------------
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    followers: Mapped[list["Follower"]] = relationship(
        back_populates="followed",
        foreign_keys="Follower.user_to_id"
    )
    following: Mapped[list["Follower"]] = relationship(
        back_populates="follower",
        foreign_keys="Follower.user_from_id"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    #-------------------RELACIONES-------------------------------------------
    follower: Mapped["User"] = relationship(
        back_populates="following",
        foreign_keys=[user_from_id]
    )
    followed: Mapped["User"] = relationship(
        back_populates="followers",
        foreign_keys=[user_to_id]
    )


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    #-------------------RELACIONES-------------------------------------------
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media_items: Mapped[list["Media"]] = relationship(back_populates="post")


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    #-------------------RELACIONES-------------------------------------------
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class Media(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum("image", "video", name="media_type"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    #-------------------RELACIONES-------------------------------------------
    post: Mapped["Post"] = relationship(back_populates="media_items")
