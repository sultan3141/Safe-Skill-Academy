from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """
    Allows access only to users who have an associated Teacher record.
    """
    def has_permission(self, request, view):
        try:
            return hasattr(request.user, 'id') and request.user.is_authenticated and \
                __import__('api').models.Teacher.objects.filter(user=request.user).exists()
        except Exception:
            # fall back - safer to return False than raise
            return False

class IsOwnerOrTeacher(BasePermission):
    """
    For student-only views - ensure the request.user is the student (owner).
    """
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user
