from django.shortcuts import render, get_object_or_404, HttpResponse
from .forms import CommentForm, LikeForm
from django.views.generic.list import ListView
from hitcount.views import HitCountDetailView
from collections import Counter


from django.http import HttpResponseRedirect
from my_blog.models import Post, Comment
from django.urls import reverse


# def blog_index(request):
#     """View of all posts from newest"""
#     posts = Post.objects.all().order_by('-created_on')
#     context = {
#         "posts": posts,
#     }
#     return render(request, "blog_index.html", context)


def blog_category(request, category):
    """View of all posts in dedicated category"""
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    """View one post with details"""
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # validation of field's correctness
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    #likes = Comment.objects.filter(likes=likes)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog_details.html", context)


def blog_post_like(request, pk):
    #likes_counter = 0
    post = Post.objects.get(pk=pk)
    like_form = LikeForm()
    if request.POST.get('blogpost_id'):
        likes_counter, created = Counter.objects.get_or_create(post.liked)
        likes_counter.count = likes_counter.count + 1
        likes_counter.save()
    return HttpResponse(likes_counter.count)
   # if "blogpost_id" in request.POST:
   #      likes_counter = +1
   #      like_form = LikeForm(request.POST)
   #      if like_form.is_valid():
   #          like = Post(
   #              liked=likes_counter
   #          )
   #          like.save()

        #post_obj = Post.objects.get(id=pk)
        #post_obj.liked.add(str(likes_counter))
        # post.number_of_likes.liked += 1
        # post.number_of_likes.liked.save()
        #like, created = Like.objects.get_or_create(user=user, post_id=post_id)
    #context = {"liked": likes_counter}
    # context = {
    #     "post": post,
    #     "liked": like,
    # }
    #return render(request, "blog_details.html", {'liked': likes_counter})
    #return HttpResponseRedirect(reverse('blogpost-detail', args=[str(pk)]))
    #return render(request, "blog_details.html", context)


# class BlogPostDetailView():
#     model = Post
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
#         liked = True
#         if likes_connected.likes.filter(id=self.request.user.id).exists():
#             liked = False
#         data['number_of_likes'] = likes_connected.number_of_likes()
#         data['post_is_liked'] = liked
#         return data

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog_index.html'


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog_details.html'
    context_object_name = 'post'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context
