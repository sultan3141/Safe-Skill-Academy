from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views
from .views import (
    StudentEnrollmentRequestCreateAPIView,
    StudentEnrollmentRequestListAPIView,
    TeacherEnrollmentRequestListAPIView,
    TeacherEnrollmentRequestUpdateAPIView,
    CourseCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    CourseMaterialListCreateAPIView,
    CourseMaterialDetailAPIView,
    CourseVariantDeleteAPIView,
    CourseVariantItemDeleteAPIView,
)
# Router for model APIs
router = DefaultRouter()
router.register(r'teachers', api_views.TeacherViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'courses', api_views.CourseViewSet)
router.register(r'variants', api_views.VariantViewSet)
router.register(r'variant-items', api_views.VariantItemViewSet)
router.register(r'questions', api_views.QuestionAnswerViewSet)
router.register(r'messages', api_views.QuestionAnswerMassageViewSet)
router.register(r'completed-courses', api_views.CompletedCourseViewSet)
router.register(r'enrolled-courses', api_views.EnrolledCourseViewSet)
router.register(r'notes', api_views.NoteViewSet)
router.register(r'reviews', api_views.ReviewViewSet)
router.register(r'notifications', api_views.NotificationViewSet)
router.register(r'countries', api_views.CountryViewSet)


urlpatterns = [
    # Auth endpoints
    path('user/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='register'),

    # Model endpoints
    path('', include(router.urls)),
    #student api endpoint
    path('student/summery/<user_id>/', api_views.StudentSummeryAPIView.as_view(), name='student-summery'),
    path('student/course-list/<user_id>/', api_views.StudentCourseListAPIView.as_view(), name='student-courses'),
    path('student/course-detail/<user_id>/<enrollment_id>/', api_views.StudentCourseDetailAPIView.as_view(), name='student-course-detail'),
    path('student/course-completed/', api_views.StudentCourseCompletedCreateAPIView.as_view(), name='student-course-completed'),
    path('student/course-Note-create/', api_views.StudentNoteCreateAPIView.as_view(), name='student-course-create'),
    path('student/course-Note-detail/', api_views.StudentNoteDetailAPIView.as_view(), name='student-course-detail'),
    path('student/rate-course/', api_views.StudentRateCourseCreateAPIView.as_view(), name='student-course-rate'),
    path('student/review-detail/', api_views.StudentRateCourseUpdateAPIView.as_view(), name='student-course-rate-detail'),
    path('student/wishlist-create/', api_views.StudentWishlistCreateAPIView.as_view(), name='student-wishlist-create'),
    path('student/enrollment-requests/create/', StudentEnrollmentRequestCreateAPIView.as_view(), name='student-enrollment-request-create'),
    path('student/enrollment-requests/my/', StudentEnrollmentRequestListAPIView.as_view(), name='student-enrollment-request-list'),

    # Teacher endpoints
    path('teacher/enrollment-requests/', TeacherEnrollmentRequestListAPIView.as_view(), name='teacher-enrollment-request-list'),
    path('teacher/enrollment-requests/<str:request_id>/review/', TeacherEnrollmentRequestUpdateAPIView.as_view(), name='teacher-enrollment-request-review'),
    path('teacher/course-list/<int:teacher_id>/', api_views.TeacherCourseListAPIView.as_view(), name='teacher-course-list'),
    path('teacher/review-list/<int:teacher_id>/', api_views.TeacherReviewListAPIView.as_view(), name='teacher-review-list'),
    path('teacher/review-detail/<int:teacher_id>/<int:review_id>/', api_views.TeacherReviewDetailAPIView.as_view(), name='teacher-review-detail'),
    path('teacher/student-list/<int:teacher_id>/', api_views.TeacherStudentListAPIView.as_view({'get':'list'}), name='teacher-student-list'), 
    path('teacher/courses/create/', CourseCreateAPIView.as_view(), name='teacher-course-create'),
    path('teacher/courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='teacher-course-detail'),
    path('teacher/variant-delete/<int:teacher_id>/<int:course_id>/<int:variant_id>/', api_views.CourseVariantDeleteAPIView.as_view(), name='course-variant-delete'),
    path('teacher/variant-item-delete/<int:teacher_id>/<int:course_id>/<int:variant_id>/<int:variant_item_id>/', api_views.CourseVariantItemDeleteAPIView.as_view(), name='course-variant-item-delete'), 

     # Course materials (list/create own materials; filter by ?course=<id>)
    path('teacher/materials/', CourseMaterialListCreateAPIView.as_view(), name='teacher-materials-list-create'),
    path('teacher/materials/<str:material_id>/', CourseMaterialDetailAPIView.as_view(), name='teacher-materials-detail'),



]
