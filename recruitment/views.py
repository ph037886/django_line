from django.shortcuts import render
from .models import RecruitmentPost

def post_list(request):
    posts = RecruitmentPost.objects.filter(is_published=True)
    return render(request, "recruitment/post_list.html", {"posts": posts})
# Create your views here.
