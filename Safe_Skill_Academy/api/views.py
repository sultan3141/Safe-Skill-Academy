from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from userauths.models import User
import random
from rest_framework.generics import CreateAPIView


from api import serializer as api_serializer
from .models import (
    Teacher, Category, Course, Variant, VariantItem,
    Question_Answer, Question_Answer_Massage,
    CompletedCourse, EnrolledCourse, Note, Review,
    Notification, country
)
from .serializer import (
    TeacherSerializer, CategorySerializer, CourseSerializer, VariantSerializer, VariantItemSerializer,
    QuestionAnswerSerializer, RateCourseSerializer, QuestionAnswerMassageSerializer,
    CompletedCourseSerializer, EnrolledCourseSerializer, NoteSerializer, ReviewSerializer,
    NotificationSerializer, CountrySerializer
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
        

