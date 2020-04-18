from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def wait_authorization_message_view(request):
    user = request.user
    if not user.has_pending_authorization:
        return redirect("hcap:index")
    return render(request, "hcap/wait_authorization.html", {})
