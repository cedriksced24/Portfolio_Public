from django.urls import path
from . import views

urlpatterns = [
    path("", views.editor, name="editor"),
    path("save/", views.save_page, name="save_page"),
    path("pages/<int:book_id>/", views.get_pages, name="get_pages"),
    path("load/<int:page_id>/", views.load_page, name="load_page"),
    path("delete/<int:page_id>/", views.delete_page, name="delete_page"),
    path("all-pages/<int:book_id>/", views.get_all_pages, name="get_all_pages"),
    path("create-book/", views.create_book, name="create_book"),
    path("delete-book/<int:book_id>/", views.delete_book, name="delete_book"),
    path("update-page/<int:page_id>/", views.update_page, name="update_page"),
]
