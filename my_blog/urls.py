from django.urls import path, include
from my_blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_index'),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category"),
    path("<int:pk>/", views.blog_post_like, name="post_like"),
    path("<int:pk>/", views.blog_post_like, name="comment_like"),
    path('<slug:slug>/', views.PostDetailView, name='detail'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount'))
]