import pandas as pd

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from bot.models import MemberInfo, RecruitmentEvent


@staff_member_required
def member_dashboard(request):
    qs = MemberInfo.objects.all().values(
        "name",
        "phone",
        "email",
        "graduate_year",
        "live_site",
        "consent_recruitment",
        "is_blocked",
        "created_at",
        "have_license",
        "note",
    )

    df = pd.DataFrame(list(qs))

    df=df[df["consent_recruitment"]==True]
    df=df[df["is_blocked"]==False]
    
    qs2=RecruitmentEvent.objects.all().values(
        'event_date',
        'event_name'
    )
    
    event_date=pd.DataFrame(list(qs2))
    
    
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")
        event_date['event_date']= pd.to_datetime(event_date["event_date"]).dt.strftime("%Y-%m-%d")
        
        df=pd.merge(df,event_date,how='left',left_on='created_at',right_on='event_date',)

        df = df.rename(columns={
            "name": "姓名",
            "phone": "電話",
            "email": "E-mail",
            "graduate_year": "畢業年",
            "live_site": "居住地",
            "created_at": "建立時間",
            "have_license": "已考上執照",
            "note": '備註',
            'event_name': '徵才活動名稱',
        })

        display_columns = [
            "姓名",
            "電話",
            "E-mail",
            "畢業年",
            "居住地",
            "建立時間",
            "已考上執照",
            '備註',
            '徵才活動名稱',
        ]

        df = df[display_columns]
        table_html = df.to_html(
            classes="display member-table",
            index=False,
            border=0,
            escape=False,
            table_id="memberTable",
        )
    else:
        table_html = ""

    return render(request, "dashboard/member_dashboard.html", {
        "table_html": table_html,
        "count": len(df),
    })