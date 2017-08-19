from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm
# from tinymce.widgets import TinyMCE
# from comments.forms import CommentForm
# from comments.models import Comment
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


# Create post
@login_required(login_url='/login/google-oauth2/?next=/')
def post_create(request):
    if not request.user.is_staff:
        if not request.user.is_superuser:
            raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Mensagem Criada")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif request.POST:
        raise
    context = {
        'input': 'Criar',
        'form': form,
        'title': 'Nova Mensagem',
    }
    return render(request, 'blog/create.html', context)


# Read blog
def post_grid(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    objf4 = queryset_list[:3]
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)).distinct()
    paginator = Paginator(queryset_list, 7)
    pnumb = paginator.page_range
    page_request_var = "p"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        'request': request,
        'user': request.user,
        'pnumb': pnumb,
        "objlist": queryset,
        "objf4": objf4,
        "page_request_var": page_request_var,
        'today': today,
    }
    return render(request, 'blog/grid.html', context)


# Read post
def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    # initial_data = {
    #     'content_type': instance.get_content_type,
    #     'object_id': instance.id
    # }
    # form = CommentForm(request.POST or None, initial=initial_data)
    # if form.is_valid() and request.user.is_authenticated():
    #     c_type = form.cleaned_data.get('content_type')
    #     content_type = ContentType.objects.get(model=c_type)
    #     obj_id = form.cleaned_data.get('object_id')
    #     content_data = form.cleaned_data.get('content')
    #     parent_obj = None
    #     try:
    #         parent_id = int(request.POST.get('parent_id'))
    #     except:
    #         parent_id = None
    #     if parent_id:
    #         parent_qs = Comment.objects.filter(id=parent_id)
    #         if parent_qs.exists() and parent_qs.count() == 1:
    #             parent_obj = parent_qs.first()
    #     new_comment, created = Comment.\
    #         objects.get_or_create(
    #             user=request.user,
    #             content_type=content_type,
    #             object_id=obj_id,
    #             content=content_data,
    #             parent=parent_obj,
    #         )
    #     return HttpResponseRedirect(
    #         new_comment.content_object.get_absolute_url()
    #     )
    # comments = instance.comments
    context = {
        # 'comments': comments,
        'instance': instance,
        'title': instance.title,
        'share_string': share_string,
        # 'form': form,
    }
    return render(request, 'blog/detail.html', context)


# Update post
@login_required(login_url='/login/google-oauth2/?next=/')
def post_update(request, slug=None):
    if not request.user.is_staff:
        if not request.user.is_superuser:
            raise Http404
    instance = get_object_or_404(Post.objects.filter(slug=slug))
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=instance
    )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Mensagem Editada")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'input': 'Gravar',
        'instance': instance,
        'title': 'Editar: ' + instance.title,
        'form': form,
    }
    return render(request, 'blog/create.html', context)


# Delete a post
@login_required(login_url='/login/google-oauth2/?next=/')
def post_delete(request, slug=None):
    if not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Mensagem Apagada")
    return redirect('blog:grid')
