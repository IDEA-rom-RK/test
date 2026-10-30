
from .storage import get_avatar_url


def header_avatar(request):
    avatar_url = None

    if request.user.is_authenticated:
        try:
            profile = request.user.profile

            if profile.avatar:
                avatar_url = get_avatar_url(profile.avatar)

        except Exception:
            avatar_url = None

    return {
        "header_avatar_url": avatar_url
    }
