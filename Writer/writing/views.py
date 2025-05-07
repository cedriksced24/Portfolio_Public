from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Post, Book, Page
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def post_editor(request):
    posts = Post.objects.order_by("-created_at")
    return render(request, "writing/editor.html", {"posts": posts})


@csrf_exempt
def save_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post.objects.create(title=title, content=content)
        return JsonResponse({"id": post.id, "title": post.title})


@csrf_exempt
def load_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return JsonResponse({"id": post.id, "title": post.title, "content": post.content})


@csrf_exempt
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return JsonResponse({"status": "deleted"})


def editor(request):
    books = Book.objects.all()
    return render(request, "writing/editor.html", {"books": books})


@csrf_exempt
def save_page(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not book_id:
            return JsonResponse({"error": "Missing book_id"}, status=400)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book not found"}, status=404)

        page = Page.objects.create(book=book, title=title, content=content)
        return JsonResponse({"id": page.id, "title": page.title})


@csrf_exempt
def get_pages(request, book_id):
    pages = Page.objects.filter(book_id=book_id).order_by("order", "-created_at")
    data = [{"id": page.id, "title": page.title} for page in pages]
    return JsonResponse(data, safe=False)


@csrf_exempt
def load_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    return JsonResponse({"id": page.id, "title": page.title, "content": page.content})


@csrf_exempt
def delete_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.delete()
    return JsonResponse({"status": "deleted"})


def get_all_pages(request, book_id):
    pages = Page.objects.filter(book_id=book_id).order_by("order", "created_at")
    data = [
        {"id": page.id, "title": page.title, "content": page.content} for page in pages
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        book = Book.objects.create(title=title)
        return JsonResponse({"id": book.id, "title": book.title})


@csrf_exempt
def delete_book(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return JsonResponse({"status": "deleted"})


@csrf_exempt
def update_page(request, page_id):
    if request.method == "POST":
        page = get_object_or_404(Page, id=page_id)
        new_title = request.POST.get("title", page.title)
        new_content = request.POST.get("content", page.content)

        print("🔄 update_page CALLED")
        print("🆔 page.id:", page.id)
        print("📄 new title:", new_title)
        print("✏️ new content (preview):", new_content[:100])

        page.title = new_title
        page.content = new_content
        page.save()
        return JsonResponse({"status": "updated"})
