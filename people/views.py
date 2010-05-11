@login_required
def view_profile(request):
    profile = request.user.get_profile()
    url = profile.url
