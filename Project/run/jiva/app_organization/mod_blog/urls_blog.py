
from django.urls import path, include

from app_organization.mod_blog import views_blog


urlpatterns = [
    # app_organization/blogs: DB/Model: Blog
    path('list_blogs/<int:organization_id>/', views_blog.list_blogs, name='list_blogs'),
    path('list_deleted_blogs/<int:organization_id>/', views_blog.list_deleted_blogs, name='list_deleted_blogs'),
    path('create_blog/<int:organization_id>/', views_blog.create_blog, name='create_blog'),
    path('edit_blog/<int:organization_id>/<int:blog_id>/', views_blog.edit_blog, name='edit_blog'),
    path('delete_blog/<int:organization_id>/<int:blog_id>/', views_blog.delete_blog, name='delete_blog'),
    path('permanent_deletion_blog/<int:organization_id>/<int:blog_id>/', views_blog.permanent_deletion_blog, name='permanent_deletion_blog'),
    path('restore_blog/<int:organization_id>/<int:blog_id>/', views_blog.restore_blog, name='restore_blog'),
    path('view_blog/<int:organization_id>/<int:blog_id>/', views_blog.view_blog, name='view_blog'),
    
    path('big_picture_blog_view/<int:organization_id>/<slug:slug>/', views_blog.big_picture_blog_view, name='big_picture_blog_view'),
]
