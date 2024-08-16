from django.urls import path
from apps.projects.views.project_views import ProjectsListAPIView, ProjectDetailAPIView
from apps.projects.views.project_file_views import ProjectFileListAPIView


urlpatterns = [
    path('', ProjectsListAPIView.as_view()),
    path('<int:pk>/', ProjectDetailAPIView.as_view()),
    path('files/', ProjectFileListAPIView.as_view()),
]