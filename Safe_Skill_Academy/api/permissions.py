from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import Teacher, Course

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Allow access if user is staff OR has a Teacher object (linked to user).
    Use for endpoints that require teacher identity.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        return Teacher.objects.filter(user=request.user).exists()

class IsCourseOwnerOrAdmin(permissions.BasePermission):
    """
    Object permission: allow if user is admin OR the teacher who owns the course/material.
    Works for Course and CourseMaterial objects.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # course object
        if isinstance(obj, Course):
            return obj.teacher.user == request.user
        # material object
        try:
            return obj.teacher.user == request.user
        except Exception:
            return False

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
