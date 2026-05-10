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


def post_detail(request, post_uuid):
    post = get_object_or_404(
        RecruitmentPost,
        uuid=post_uuid,
        is_published=True
    )

    return render(
        request,
        "recruitment/post_detail.html",
        {"post": post}
    )