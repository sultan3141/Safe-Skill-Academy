from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from rest_framework.parsers import MultiPartParser, FormParser
import random
from rest_framework.exceptions import ValidationError
from .models import Quiz, QuizQuestion, QuizAnswer 
from rest_framework import generics
from .models import Quiz, StudentQuizAttempt
from .serializer import QuizSerializer, StudentQuizAttemptSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from .permissions import IsTeacher, IsOwnerOrTeacher
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import generics, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from .permissions import IsTeacherOrAdmin, IsCourseOwnerOrAdmin
from api import serializer as api_serializer
from .models import (
    Teacher, Category, Wishlist, CourseMaterial, EnrollmentRequest,  Course,  Variant, VariantItem,
    Question_Answer, Question_Answer_Massage, CompletedCourse, EnrolledCourse, Note, Review, Notification, country,
)
from .serializer import (
    TeacherSerializer, CategorySerializer, CourseSerializer, QuizSerializer, QuizQuestionSerializer, QuizAnswerSerializer, CourseCreateUpdateSerializer, CourseMaterialSerializer, CourseSerializer, VariantSerializer, VariantItemSerializer,
    QuestionAnswerSerializer, RateCourseSerializer, QuestionAnswerMassageSerializer,QuestionAnswerCreateSerializer,
    CompletedCourseSerializer, EnrolledCourseSerializer, EnrollmentRequestCreateSerializer, EnrollmentRequestListSerializer, NoteSerializer, ReviewSerializer,
    NotificationSerializer, CountrySerializer,WishlistSerializer
)

# -------------------------
# AUTH & USER MANAGEMENT
# -------------------------

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = [AllowAny]

def generate_random_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


# -------------------------
# MODEL VIEWSETS
# -------------------------

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer

class VariantItemViewSet(viewsets.ModelViewSet):
    queryset = VariantItem.objects.all()
    serializer_class = VariantItemSerializer

class QuestionAnswerViewSet(viewsets.ModelViewSet):
    queryset = Question_Answer.objects.all()
    serializer_class = QuestionAnswerSerializer

class QuestionAnswerMassageViewSet(viewsets.ModelViewSet):
    queryset = Question_Answer_Massage.objects.all()
    serializer_class = QuestionAnswerMassageSerializer

class CompletedCourseViewSet(viewsets.ModelViewSet):
    queryset = CompletedCourse.objects.all()
    serializer_class = CompletedCourseSerializer

class EnrolledCourseViewSet(viewsets.ModelViewSet):
    queryset = EnrolledCourse.objects.all()
    serializer_class = EnrolledCourseSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = country.objects.all()
    serializer_class = CountrySerializer

class StudentSummeryAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.StudentSummerySerializer

    def queryset(self):
        user_id=self.kwargs['user_id']
        user=User.objects.get(id=user_id)

        total_courses=EnrolledCourse.objects.filter(user=user).count()
        completed_courses=CompletedCourse.objects.filter(user=user).count()
        return [{
            "total_courses":total_courses,
            "completed_courses":completed_courses,
        }]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 

class StudentCourseListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.EnrolledCourseSerializer

    def get_queryset(self):
        user_id=self.kwargs['user_id']
        user=User.objects.get(id=user_id)
        return EnrolledCourse.objects.filter(user=user).order_by('-enrolled_at')  

class StudentCourseDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.EnrolledCourseSerializer
    lookup_field = 'enrolled_id'

    def get_queryset(self):
        user_id=self.kwargs['user_id']
        enrolled_id=self.kwargs['enrollment_id']
        user=User.objects.get(id=user_id)
        enrollment_id=EnrolledCourse.objects.get(enrolled_id=enrolled_id)
        return EnrolledCourse.objects.filter(user=user, course=course)

class StudentCourseCompletedCreateAPIView(CreateAPIView):
    serializer_class =CompletedCourseSerializer
    permission_classes=[AllowAny]
    
    def create(self, request, *args, **kwargs):
        course_id= request.data.get('course_id')
        user_id= request.data.get('student_id')
        variant_item_id= request.data.get('variant_item_id')
        
        user= User.objects.get(id=user_id)
        course= Course.objects.get(id=course_id)
        variant_item= VariantItem.objects.get(variant_item_id=variant_item_id)
        
        completed_lessons= CourseLesson.objects.filter(user=user, course=course, variant_item=variant_item).first()
        if completed_lessons:
            completed_lessons.delete()
            return Response({'detail': 'Course already marked as completed.'})
        else:
            CourseLesson.objects.create(user=user, course=course, variant_item=variant_item)
            return Response({'detail': 'Course marked as completed.'})

class StudentNoteCreateAPIView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        user_id=self.kwargs['user_id']
        enrollment_id=self.kwargs['enrollment_id']
        
        user=User.objects.get(user_id=user_id)
        enrolled=EnrolledCourse.objects.get(enrollment_id=enrollment_id)
        return Note.objects.filter(user=user,enrollment=enrolled)
    
    def create(self, request, *args, **kwargs):
        user_id=request.data['user_id']
        enrollment_id=request.data['enrollment_id']
        note=request.data['note']
        title=request.data['title']
        
        user=User.objects.get(user_id=user_id)
        enrolled=EnrolledCourse.objects.get(enrollment_id=enrollment_id) 
        Note.objects.create(user=user,enrollment=enrolled,note=note,title=title)
        
        return Response({"message":"Note created successfully"},status=status.HTTP_201_CREATED)

class StudentNoteDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NoteSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        user_id=self.kwargs['user_id']
        enrollment_id=self.kwargs['enrollment_id']
        note_id=self.kwargs['note_id']
        
        user=User.objects.get(user_id=user_id)
        enrolled=EnrolledCourse.objects.get(enrollment_id=enrollment_id) 
        note=Note.objects.get(user=user,enrollment=enrolled)
        return note  

class StudentRateCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = RateCourseSerializer
    permission_classes=[AllowAny]
    
    def create(self, request, *args, **kwargs):
        user_id=request.data['user_id']
        course_id=request.data['course_id']
        rating=request.data['rating']
        review=request.data['review']
        
        user=User.objects.get(user_id=user_id)
        course=Course.objects.get(course_id=course_id) 
        
        Review.objects.create(user=user,course=course,rating=rating,review=review,active=True)
        return Response({"message":"Course rated successfully"},status=status.HTTP_201_CREATED)
            
   
class StudentRateCourseUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        user_id=self.kwargs['user_id']
        review_id=self.kwargs['review_id']
        
        user=User.objects.get(user_id=user_id)
        return Review.objects.get(user=user,review_id=review_id)


class StudentWishlistCreateAPIView(generics.CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the user from request
        serializer.save(user=self.request.user)


# Student: create enrollment request (multipart/form-data for payment_slip)
class StudentEnrollmentRequestCreateAPIView(generics.CreateAPIView):
    serializer_class = EnrollmentRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # student comes from request.user inside serializer.create
        serializer.save()

# Student: list my enrollment requests
class StudentEnrollmentRequestListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentRequestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return EnrollmentRequest.objects.filter(student=user).order_by('-created_at')

# Teacher: list enrollment requests for their courses
class TeacherEnrollmentRequestListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentRequestListSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        # find teacher by request.user
        teacher = get_object_or_404(Teacher, user=self.request.user)
        # all enrollment requests for courses taught by this teacher
        return EnrollmentRequest.objects.filter(course__teacher=teacher).order_by('-created_at')

# Teacher: approve or reject
class TeacherEnrollmentRequestUpdateAPIView(generics.UpdateAPIView):
    """
    PATCH body example to approve:
      { "action": "approve" }
    to reject:
      { "action": "reject", "teacher_note": "reason" }
    """
    serializer_class = EnrollmentRequestListSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]
    lookup_field = 'request_id'
    queryset = EnrollmentRequest.objects.all()

    def patch(self, request, *args, **kwargs):
        enrollment_request = self.get_object()
        teacher = get_object_or_404(Teacher, user=request.user)
        action = request.data.get('action')

        if action not in ('approve', 'reject'):
            return Response({"detail": "action must be 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

        if enrollment_request.course.teacher != teacher:
            return Response({"detail": "You are not allowed to review requests for this course."}, status=status.HTTP_403_FORBIDDEN)

        if action == 'approve':
            # approve and create enrolled course atomically
            with transaction.atomic():
                enrolled, created = enrollment_request.approve(reviewer=teacher)
                serializer = self.get_serializer(enrollment_request)
                return Response({
                    "detail": "Enrollment request approved.",
                    "enrolled_created": created,
                    "enrolled_id": getattr(enrolled, 'enrolled_id', None),
                    "request": serializer.data
                }, status=status.HTTP_200_OK)

        # reject
        note = request.data.get('teacher_note', '')
        enrollment_request.reject(reviewer=teacher, note=note)
        serializer = self.get_serializer(enrollment_request)
        return Response({"detail": "Enrollment request rejected.", "request": serializer.data}, status=status.HTTP_200_OK)

class TeacherCourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        teacher=Teacher.objects.get()
        return Course.objects.filter(teacher=teacher)
    
class TeacherReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        return Review.objects.filter(course__teacher=teacher)

class TeacherReviewDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        teacher_id=self.kwargs['teacher_id']
        review_id=self.kwargs['review_id']
        
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        return Review.objects.get(course__teacher=teacher,review_id=review_id)
    
class TeacherStudentListAPIView(viewsets.ViewSet):
    def list(self, request, teacher_id=None):
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        enrolled_courses=EnrolledCourse.objects.filter(teacher=teacher)
        unique_student_ids=set()
        students=[]
        for course in enrolled_courses:
            if course.user_id not in unique_student_ids:
                user=User.objects.get(user_id=course.user_id)
                student={
                    "full_name":user.profile.full_name,
                    "image":user.profile.image,
                    "country":user.profile.country,
                    "data":course.date
                    }
                students.append(student)
                unique_student_ids.add(course.user_id)
        return Response(students)



# Teacher: Create Course
class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdmin]
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        # get Teacher instance for current user
        try:
            teacher = Teacher.objects.get(user=self.request.user)
        except Teacher.DoesNotExist:
            raise PermissionDenied("Only teachers can create courses.")
        serializer.save(teacher=teacher)

# Teacher: Retrieve / Update (partial ok) / Delete their course
class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseOwnerOrAdmin]

    # object-level permission uses IsCourseOwnerOrAdmin.has_object_permission

    def perform_update(self, serializer):
        # Ensure teacher cannot change owner field
        instance = serializer.instance
        # If user is not admin, ensure user is the owner
        if not self.request.user.is_staff:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            if instance.teacher != teacher:
                raise PermissionDenied("You do not have permission to edit this course.")
            serializer.save(teacher=instance.teacher)
        else:
            serializer.save()

# Teacher + Admin: List / Create materials and filter by course via ?course=<id>
class CourseMaterialListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = CourseMaterial.objects.all().select_related('course', 'teacher')
        # if teacher (non-staff) only return own materials
        if not self.request.user.is_staff:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            qs = qs.filter(teacher=teacher)
        # optional filter by course id -> ?course=123
        course_id = self.request.query_params.get('course')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

    def perform_create(self, serializer):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        course = serializer.validated_data.get('course')
        if course.teacher != teacher:
            raise PermissionDenied("You can only add materials to your own courses.")
        serializer.save(teacher=teacher)

# Teacher/Admin: Retrieve / Update / Delete a material
class CourseMaterialDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourseOwnerOrAdmin]
    lookup_field = 'material_id'

    def perform_update(self, serializer):
        obj = self.get_object()
        # only owner or staff allowed (IsCourseOwnerOrAdmin already checks)
        if not self.request.user.is_staff and obj.teacher.user != self.request.user:
            raise PermissionDenied("You may not edit this material.")
        # keep teacher field unchanged
        serializer.save(teacher=obj.teacher)

class CourseVariantDeleteAPIView(generics.DestroyAPIView):
    serializer_class = VariantSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        teacher_id=self.kwargs['teacher_id']
        course_id=self.kwargs['course_id']
        variant_id=self.kwargs['variant_id']
        
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        course=Course.objects.get(teacher=teacher, course_id=course_id)
        return Variant.objects.get(course=course, variant_id=variant_id)
    
class CourseVariantItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = VariantItemSerializer
    permission_classes=[AllowAny]
    
    def get_object(self):
        teacher_id=self.kwargs['teacher_id']
        course_id=self.kwargs['course_id']
        variant_id=self.kwargs['variant_id']
        variant_item_id=self.kwargs['variant_item_id']
        
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        course=Course.objects.get(teacher=teacher, course_id=course_id)
        variant=Variant.objects.get(course=course, variant_id=variant_id)
        return VariantItem.objects.get(variant=variant, variant_item_id=variant_item_id)

class QuestionAnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionAnswerCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()



# Create Quiz
class TeacherQuizListCreateAPIView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all().order_by('-created_at')
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        return Quiz.objects.filter(teacher=teacher)

    def perform_create(self, serializer):
        teacher = Teacher.objects.get(user=self.request.user)
        course = serializer.validated_data['course']
        if course.teacher != teacher:
            raise ValidationError("You can only create quizzes for your own courses.")
        serializer.save(teacher=teacher)


# Quiz Detail
class TeacherQuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'quiz_id'

    def perform_update(self, serializer):
        teacher = Teacher.objects.get(user=self.request.user)
        if serializer.instance.teacher != teacher:
            raise ValidationError("You can only update your own quiz.")
        serializer.save()


# Add questions to quiz
class TeacherQuizQuestionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = QuizQuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return QuizQuestion.objects.filter(quiz__quiz_id=quiz_id)

    def perform_create(self, serializer):
        quiz_id = self.kwargs['quiz_id']
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        teacher = Teacher.objects.get(user=self.request.user)
        if quiz.teacher != teacher:
            raise ValidationError("You can only add questions to your own quiz.")
        serializer.save(quiz=quiz)


# Add answers to a question
class TeacherQuizAnswerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = QuizAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return QuizAnswer.objects.filter(question_id=question_id)

    def perform_create(self, serializer):
        question_id = self.kwargs['question_id']
        question = QuizQuestion.objects.get(id=question_id)
        teacher = Teacher.objects.get(user=self.request.user)
        if question.quiz.teacher != teacher:
            raise ValidationError("You can only add answers to your own quiz questions.")
        serializer.save(question=question)



class StudentQuizListAPIView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Quiz.objects.filter(course_id=course_id)


class StudentSubmitQuizAPIView(generics.CreateAPIView):
    serializer_class = StudentQuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class StudentQuizResultAPIView(generics.RetrieveAPIView):
    serializer_class = StudentQuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        student_id = self.kwargs['student_id']
        attempt_id = self.kwargs['attempt_id']
        return StudentQuizAttempt.objects.get(student_id=student_id, attempt_id=attempt_id)
