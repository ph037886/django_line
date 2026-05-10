from django.shortcuts import get_object_or_404, render
from .models import RecruitmentPost


def post_list(request):
    posts = RecruitmentPost.objects.filter(
        is_published=True
    )

    return render(
        request,
        "recruitment/post_list.html",
        {"posts": posts}
    )


def post_detail(request, post_short_id):
    post = get_object_or_404(
        RecruitmentPost,
        short_id=post_short_id,
        is_published=True
    )

    return render(
        request,
        "recruitment/post_detail.html",
        {"post": post}
    )