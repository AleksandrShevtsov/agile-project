from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from apps.projects.models.project import *
from apps.projects.models.project_file import *
from apps.projects.serializers.project_file_serializers import (
    AllProjectFilesSerializer,
    CreateProjectFileSerializer,
)


class ProjectFileListAPIView(APIView):
    def get_objects(self, project_name=None):
        if project_name:
            project_file = ProjectFile.objects.filter(
                project__name=project_name
            )
            return project_file
        return ProjectFile.objects.all()

    def get(self, request: Request) -> Response:
        project_name = request.query_params.get('project')

        project_files = self.get_objects(project_name)
        if not project_files.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT
                            )
        serializer = AllProjectFilesSerializer(project_files, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        file_content = request.FILES["file"]

        project_id = request.data["project_id"]
        project = get_object_or_404(Project, pk=project_id)
        serializer = CreateProjectFileSerializer(data=request.data, context={"raw_file": file_content, })
