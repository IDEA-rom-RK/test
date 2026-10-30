
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from .storage import upload_avatar, get_avatar_url
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET


def base(request):
    return render(request, "base.html")


def home(request):
    return render(request, "HBase.html")



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "Register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("profile")
    else:
        form = LoginForm(request)

    return render(request, "log.html", {"form": form})





@login_required(login_url="log")
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        profile.description = request.POST.get(
            "description", ""
        ).strip()

        profile.other_interests = request.POST.get(
            "other_interests", ""
        ).strip()

        profile.interests = {
            "selected": request.POST.getlist("interests")
        }

        profile.search_goals = request.POST.getlist(
            "search_goals"
        )

        profile.important = request.POST.getlist(
            "important"
        )

        # Загружаем новый аватар, если пользователь выбрал файл
        avatar_file = request.FILES.get("avatar")

        if avatar_file:
            try:
                profile.avatar = upload_avatar(
                    avatar_file,
                    request.user.id
                )
            except ValueError as error:
                messages.error(request, str(error))
                return redirect("profile")
            except Exception:
                messages.error(
                    request,
                    "Не удалось загрузить изображение. Попробуйте позже."
                )
                return redirect("profile")

        profile.save()

        messages.success(request, "Профиль успешно сохранён!")

        return redirect("profile")

    selected_interests = profile.interests.get(
        "selected", []
    )

    avatar_url = None

    if profile.avatar:
        try:
            avatar_url = get_avatar_url(profile.avatar)
        except Exception:
            messages.error(
                request,
                "Не удалось загрузить отображение аватара."
            )

    return render(request, "profile.html", {
        "profile": profile,
        "selected_interests": selected_interests,
        "selected_goals": profile.search_goals,
        "selected_important": profile.important,
        "avatar_url": avatar_url,
    })


@login_required
@require_GET
def search_users(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"users": []})

    users = User.objects.filter(
        username__icontains=query
    ).exclude(
        id=request.user.id
    )[:10]

    results = [
        {
            "username": user.username,
        }
        for user in users
    ]

    return JsonResponse({"users": results})

def search_page(request):
    return render(request, "searching.html")