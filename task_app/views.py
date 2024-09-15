from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


class TaskListView(APIView):
    """
        View to list all tasks for the authenticated user.

        **GET** /api/tasks/

        Returns a list of tasks associated with the currently authenticated user,
        ordered by creation date with the most recent tasks first. If no tasks are found,
        a message indicating this will be returned.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            tasks = Task.objects.filter(user=user).order_by('-created_at')

            if not tasks.exists():
                return Response({"message": "No tasks found"}, status=status.HTTP_200_OK)

            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskCreateView(APIView):
    """
        View to create a new task for the authenticated user.

        **POST** /api/tasks/create/

        Requires a title for the task. If the title is missing, an error is returned.
        On success, the newly created task is returned.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            data = request.data.copy()
            data['user'] = user.id

            if not data.get('title'):
                return Response({"error": "The title field cannot be empty."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskDetailView(APIView):
    """
        View to retrieve details of a specific task.

        **GET** /api/tasks/<int:pk>/

        Retrieves the details of a task specified by its primary key (pk). Returns the task details if found
        and owned by the authenticated user. If the task does not exist or does not belong to the user,
        an appropriate error message is returned.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)

            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to access this task."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskUpdateView(APIView):
    """
        View to update a specific task.

        **PUT** /api/tasks/<int:pk>/update/

        Updates the task specified by its primary key (pk). If the title is included in the request data,
        it cannot be empty. Returns the updated task details if successful.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:

            task = Task.objects.get(pk=pk, user=request.user)

            data = request.data.copy()
            if 'title' in data and not data.get('title'):
                return Response({"error": "The title field cannot be empty."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = TaskSerializer(task, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to access this task."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDeleteView(APIView):
    """
        View to delete a specific task.

        **DELETE** /api/tasks/<int:pk>/delete/

        Deletes the task specified by its primary key (pk). Returns a success message upon successful deletion.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found or you do not have permission to delete this task."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskFilterView(APIView):
    """
        View to filter tasks based on their status.

        **GET** /api/tasks/filter/

        You can filter tasks by their status using the `status` query parameter:
        - `completed`: To get completed tasks.
        - `pending`: To get pending tasks.

        Returns the filtered list of tasks or an error if the filter is invalid.

        Permissions:
        - Requires authentication
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            status_filter = request.query_params.get('status', None)

            if status_filter is not None:
                if status_filter.lower() == 'completed':
                    tasks = Task.objects.filter(user=request.user, status=True).order_by('-created_at')
                elif status_filter.lower() == 'pending':
                    tasks = Task.objects.filter(
                        user=request.user, status=False).order_by('-created_at')
                else:
                    return Response({"error": "Invalid status filter. Use 'completed' or 'pending'."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                tasks = Task.objects.filter(user=request.user)

            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
