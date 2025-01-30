from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Post, Event
from .forms import CommentForm


# Event Views
class EventsList(generic.ListView):
    """
    Displays a list of events, paginated by 12 per page.
    """
    model = Event
    template_name = "index.html"
    paginate_by = 12


def event_detail(request, event_id):
    """
    Displays details of an individual :model:`events.Event`.

    **Context**

    ``event``
        An instance of :model:`events.Event`.

    **Template:**

    :template:`events/event_detail.html`
    """
    event = get_object_or_404(Event, id=event_id)

    return render(
        request,
        "events/event_detail.html",
        {"event": event}
    )


# Blog Views
class PostList(generic.ListView):
    """
    Displays a list of published blog posts, paginated by 6 per page.
    """
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Displays details of an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        A list of approved comments for the post.
    ``comment_count``
        The total number of approved comments for the post.
    ``comment_form``
        A form instance for adding new comments.

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )


    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html", {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )
