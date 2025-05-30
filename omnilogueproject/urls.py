from django.urls import include, path
from rest_framework.routers import DefaultRouter
from omnilogueapi.views import (
    UserViewSet,
    StoryViewSet,
    BookshelfViewSet,
    CategoryViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"stories", StoryViewSet, "story")
router.register(r"bookshelves", BookshelfViewSet, "bookshelf")
router.register(r"categories", CategoryViewSet, "category")


urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]
