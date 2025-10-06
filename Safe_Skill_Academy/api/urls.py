from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

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


]
