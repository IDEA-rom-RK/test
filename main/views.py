
from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.models import Q, Exists, OuterRef


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
    selected_interests = request.GET.getlist("interests")

    allowed_interests = {
        "game_shooter", "game_strategy", "game_rpg",
        "game_survival", "game_simulator", "game_sandbox",

        "book_fantasy", "book_detective", "book_classic",
        "book_romance", "book_history",

        "film_action", "film_comedy", "film_drama",
        "film_horror", "film_scifi",

        "music_rock", "music_pop", "music_metal",
        "music_classical", "music_electronic",

        "sport_football", "sport_basketball", "sport_swimming",
        "sport_running", "sport_other",

        "creative_drawing", "creative_animation",
        "creative_music", "creative_writing", "creative_video",
    }

    selected_interests = [
        interest for interest in selected_interests
        if interest in allowed_interests
    ]

    if not query and not selected_interests:
        return JsonResponse({"users": []})

    # Начинаем поиск со всех зарегистрированных пользователей.
    users = User.objects.exclude(pk=request.user.pk)

    # Фильтр по никнейму.
    if query:
        users = users.filter(username__icontains=query)

    # Если выбраны интересы, оставляем только пользователей,
    # у которых существует профиль с совпадающими интересами.
    if selected_interests:
        interest_filter = Q()

        for interest in selected_interests:
            interest_filter |= Q(
                interests__selected__contains=[interest]
            )

        matching_profiles = Profile.objects.filter(
            interest_filter,
            user_id=OuterRef("pk")
        )

        users = users.annotate(
            has_matching_interests=Exists(matching_profiles)
        ).filter(has_matching_interests=True)

    # Получаем максимум 10 пользователей.
    users = list(users.order_by("username")[:10])

    # Загружаем профили найденных пользователей.
    profiles = Profile.objects.filter(
        user_id__in=[user.id for user in users]
    )

    profiles_by_user = {
        profile.user_id: profile
        for profile in profiles
    }

    results = []

    for user in users:
        profile = profiles_by_user.get(user.id)

        user_interests = (
            (profile.interests or {}).get("selected", [])
            if profile else []
        )

        common_count = len(
            set(selected_interests) & set(user_interests)
        )

        results.append({
            "username": user.username,
            "common_interests_count": common_count,
        })

    return JsonResponse({"users": results})


def search_page(request):
    return render(request, "searching.html")


def anthrprofile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user).first()

    avatar_url = None

    if profile and profile.avatar:
        try:
            avatar_url = get_avatar_url(profile.avatar)
        except Exception:
            avatar_url = None

    return render(request, "userprofile.html", {
        "profile": profile,
        "profile_user": user,
        "avatar_url": avatar_url,
    })
