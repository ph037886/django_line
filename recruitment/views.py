from django.shortcuts import get_object_or_404, render
from .models import RecruitmentPost, job_bank_link


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
        RecruitmentPost.objects.prefetch_related("job_bank_links"),
        short_id=post_short_id,
        is_published=True
    )

    visible_links = post.job_bank_links.filter(job_show=True)
    
    return render(
        request,
        "recruitment/post_detail.html",
        {"post": post, 
         "visible_links": visible_links,}
    )