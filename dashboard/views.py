import pandas as pd

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from bot.models import MemberInfo


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

    if not df.empty:
        df["consent_recruitment"] = df["consent_recruitment"].map({
            True: "同意",
            False: "不同意"
        })

        df["is_blocked"] = df["is_blocked"].map({
            True: "已封鎖",
            False: "可推播"
        })

        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")

        df = df.rename(columns={
            "name": "姓名",
            "phone": "電話",
            "email": "E-mail",
            "graduate_year": "畢業年",
            "live_site": "居住地",
            "consent_recruitment": "接收徵才資訊",
            "is_blocked": "LINE狀態",
            "created_at": "建立時間",
            "have_license": "已考上執照",
            "note": '備註',
        })

        display_columns = [
            "姓名",
            "電話",
            "E-mail",
            "畢業年",
            "居住地",
            "接收徵才資訊",
            "LINE狀態",
            "建立時間",
            "已考上執照",
            '備註',
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