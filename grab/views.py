from django.contrib.auth.decorators import login_required

# --- New Social Media Style Views ---
@login_required
def notifications(request):
    # Placeholder: In a real app, fetch user notifications
    return render(request, 'grab/notifications.html', _base_context(request))

@login_required
def messages(request):
    # Placeholder: In a real app, fetch user messages/conversations
    return render(request, 'grab/messages.html', _base_context(request))

@login_required
def friends(request):
    # Placeholder: In a real app, fetch user friends/followers
    return render(request, 'grab/friends.html', _base_context(request))
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, Postform, ProfileUpdateForm, signupform
from .models import Comment, Follow, Like, Post, Profile, Save, Topic


def _base_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        profile = request.user.profile
        unread_style_count = (
            Follow.objects.filter(following=profile).count()
            + Like.objects.filter(post__profile=profile).exclude(profile=profile).count()
            + Comment.objects.filter(post__profile=profile).exclude(profile=profile).count()
        )
        return {
            'nav_saved_count': Save.objects.filter(profile=profile).count(),
            'nav_alert_count': unread_style_count,
        }
    return {
        'nav_saved_count': 0,
        'nav_alert_count': 0,
    }


def _enrich_posts(request, posts):
    posts = list(posts)
    user_profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None

    liked_post_ids = set()
    followed_profile_ids = set()
    saved_post_ids = set()
    if user_profile:
        liked_post_ids = set(Like.objects.filter(profile=user_profile).values_list('post_id', flat=True))
        followed_profile_ids = set(Follow.objects.filter(follower=user_profile).values_list('following_id', flat=True))
        saved_post_ids = set(Save.objects.filter(profile=user_profile).values_list('post_id', flat=True))

    for post in posts:
        post.is_liked = post.id in liked_post_ids
        post.is_following_author = post.profile_id in followed_profile_ids
        post.is_saved = post.id in saved_post_ids
        post.comment_form = CommentForm()
        post.preview_comments = list(post.comments.all()[:3])

    return posts


def _post_queryset():
    return (
        Post.objects.select_related('profile', 'profile__user', 'topic')
        .prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('profile', 'profile__user').order_by('-created_at'))
        )
        .annotate(
            likes_total=Count('likes', distinct=True),
            comments_total=Count('comments', distinct=True),
            saves_total=Count('saves', distinct=True),
        )
        .order_by('-id')
    )


def home(request):
    topics = Topic.objects.all()
    selected_topic_id = request.GET.get('topic')
    posts = _post_queryset()
    if selected_topic_id:
        posts = posts.filter(topic_id=selected_topic_id)

    context = {
        **_base_context(request),
        'posts': _enrich_posts(request, posts),
        'topics': topics,
        'selected_topic_id': selected_topic_id,
        'total_posts': Post.objects.count(),
        'total_creators': Profile.objects.count(),
        'trending_topics': topics[:6],
        'active_connections': Follow.objects.count(),
    }
    return render(request, "grab/index.html", context)


def signup(request):
    form = signupform()
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "grab/signup.html", {'form': form, **_base_context(request)})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('login')
    return render(request, "grab/login.html", _base_context(request))


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


@login_required
def profile(request):
    profile_obj = get_object_or_404(Profile, user=request.user)
    posts = _post_queryset().filter(profile=profile_obj)
    context = {
        **_base_context(request),
        'profiledetail': _enrich_posts(request, posts),
        'profile_obj': profile_obj,
        'profile_posts_count': Post.objects.filter(profile=profile_obj).count(),
        'recent_followers': Follow.objects.filter(following=profile_obj).select_related('follower__user')[:6],
    }
    return render(request, "grab/profile.html", context)


def search_profile(request):
    query_prof = request.GET.get('profile')
    results = Profile.objects.all()
    if request.user.is_authenticated:
        results = results.exclude(user=request.user)
    results = results.annotate(
        posts_total=Count('post'),
        followers_total=Count('followers', distinct=True),
    )
    if query_prof:
        results = results.filter(user__username__icontains=query_prof)

    return render(
        request,
        'grab/search.html',
        {'result': results, 'query_prof': query_prof, **_base_context(request)},
    )


def profile_view(request, id):
    profile = get_object_or_404(Profile, id=id)
    posts = _post_queryset().filter(profile=profile)
    is_following = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_following = Follow.objects.filter(follower=request.user.profile, following=profile).exists()
    context = {
        **_base_context(request),
        'profile': profile,
        'posts': _enrich_posts(request, posts),
        'is_following': is_following,
        'profile_posts_count': Post.objects.filter(profile=profile).count(),
    }
    return render(request, 'grab/profileview.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'grab/profile_edit.html', {'p_form': p_form, **_base_context(request)})


@login_required
def delete(request, id):
    delete_post = get_object_or_404(Post, id=id, profile=request.user.profile)
    delete_post.delete()
    return redirect('profile')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = request.user.profile
            post.save()
            return redirect('/')
    else:
        form = Postform()
    return render(request, 'grab/postform.html', {'form': form, **_base_context(request)})


@login_required
def toggle_follow(request, id):
    if request.method == 'POST':
        target_profile = get_object_or_404(Profile, id=id)
        my_profile = request.user.profile
        if my_profile != target_profile:
            follow = Follow.objects.filter(follower=my_profile, following=target_profile)
            if follow.exists():
                follow.delete()
            else:
                Follow.objects.create(follower=my_profile, following=target_profile)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_like(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        like = Like.objects.filter(profile=request.user.profile, post=post)
        if like.exists():
            like.delete()
        else:
            Like.objects.create(profile=request.user.profile, post=post)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_save(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        saved = Save.objects.filter(profile=request.user.profile, post=post)
        if saved.exists():
            saved.delete()
        else:
            Save.objects.create(profile=request.user.profile, post=post)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = request.user.profile
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def explore(request):
    topics = Topic.objects.annotate(posts_total=Count('post')).order_by('-posts_total', 'topic_name')[:8]
    creators = Profile.objects.annotate(
        posts_total=Count('post'),
        followers_total=Count('followers', distinct=True),
    ).order_by('-followers_total', '-posts_total')[:8]
    posts = _enrich_posts(request, _post_queryset()[:9])
    context = {
        **_base_context(request),
        'topics': topics,
        'creators': creators,
        'posts': posts,
    }
    return render(request, 'grab/explore.html', context)


def moments(request):
    posts = _enrich_posts(request, _post_queryset()[:12])
    return render(request, 'grab/moments.html', {'posts': posts, **_base_context(request)})


@login_required
def activity(request):
    my_profile = request.user.profile
    my_posts = Post.objects.filter(profile=my_profile)
    follow_events = Follow.objects.filter(following=my_profile).select_related('follower__user')[:8]
    like_events = Like.objects.filter(post__in=my_posts).exclude(profile=my_profile).select_related('profile__user', 'post')[:8]
    comment_events = Comment.objects.filter(post__in=my_posts).exclude(profile=my_profile).select_related('profile__user', 'post')[:8]
    context = {
        **_base_context(request),
        'follow_events': follow_events,
        'like_events': like_events,
        'comment_events': comment_events,
    }
    return render(request, 'grab/activity.html', context)


@login_required
def inbox(request):
    my_profile = request.user.profile
    conversations = Profile.objects.filter(
        Q(followers__follower=my_profile) | Q(following__following=my_profile) | Q(comments__post__profile=my_profile)
    ).exclude(id=my_profile.id).select_related('user').distinct()[:10]
    context = {
        **_base_context(request),
        'conversations': conversations,
    }
    return render(request, 'grab/inbox.html', context)


@login_required
def saved_posts(request):
    saved_ids = Save.objects.filter(profile=request.user.profile).values_list('post_id', flat=True)
    posts = _enrich_posts(request, _post_queryset().filter(id__in=saved_ids))
    return render(request, 'grab/saved.html', {'posts': posts, **_base_context(request)})


def followers_list(request, id):
    profile = get_object_or_404(Profile, id=id)
    followers = Follow.objects.filter(following=profile).select_related('follower__user')
    return render(
        request,
        'grab/follow_list.html',
        {
            'page_title': f"{profile.user.username}'s followers",
            'page_heading': 'Followers',
            'connections': followers,
            'mode': 'followers',
            'profile': profile,
            **_base_context(request),
        },
    )


def following_list(request, id):
    profile = get_object_or_404(Profile, id=id)
    following = Follow.objects.filter(follower=profile).select_related('following__user')
    return render(
        request,
        'grab/follow_list.html',
        {
            'page_title': f"{profile.user.username} is following",
            'page_heading': 'Following',
            'connections': following,
            'mode': 'following',
            'profile': profile,
            **_base_context(request),
        },
    )
