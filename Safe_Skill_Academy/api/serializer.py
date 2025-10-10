from rest_framework import serializers
from users.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import (
    Teacher, Category, Course, Variant, CourseMaterial, VariantItem,
    Question_Answer, CourseRating, Question_Answer_Massage,Quiz, QuizQuestion, QuizAnswer, StudentQuizAttempt, StudentQuizAnswer,
    CompletedCourse, EnrolledCourse, Note, Review,
    Notification, country, Wishlist, EnrollmentRequest
)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
class RegisterSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True, required=True,validators=[validate_password])    
   password2 = serializers.CharField(write_only=True, required=True)

   class Meta:
       model=User
       fields = ('full_name', 'password', 'password2', 'email')
   def validate(self, attrs):
       if attrs['password'] != attrs['password2']:
           raise serializers.ValidationError({"password": "Password fields didn't match."})
       return attrs

   def create(self, validated_data):
       user = User.objects.create(
           full_name=validated_data['full_name'],
           email=validated_data['email'],
       )
       email_username,_=user.email.split('@')
       user.username=email_username
       user.set_password(validated_data['password'])
       user.save() 
       
       return user



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class VariantItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantItem
        fields = '__all__'

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_Answer
        fields = '__all__'

class QuestionAnswerCreateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question_Answer
        fields = ['id', 'course', 'teacher', 'question', 'answer', 'created_at']
        read_only_fields = ['teacher', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        teacher = Teacher.objects.get(user=request.user)
        course = validated_data.get('course')

        # ✅ Ensure the teacher owns the course
        if course.teacher != teacher:
            raise serializers.ValidationError("You can only add questions to your own courses.")

        validated_data['teacher'] = teacher
        return super().create(validated_data)


class QuestionAnswerMassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_Answer_Massage
        fields = '__all__'

class CompletedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedCourse
        fields = '__all__'



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = country
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"


class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lectures = VariantItemSerializer(many=True, read_only=True)
    curriculum = VariantItemSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = QuestionAnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(read_only=True)   
    
    class Meta:
        model = EnrolledCourse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EnrolledCourseSerializer.self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='post':
          self.Meta.depth=0
        else:
          self.Meta.depth=1
class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    students = serializers.IntegerField(source='students', read_only=True)
    curriculum = VariantItemSerializer(many=True, read_only=True)
    lactures = serializers.IntegerField(source='lactures', read_only=True)
    average_rating = serializers.FloatField(source='average_rating', read_only=True)
    rating_count = serializers.IntegerField(source='rating_count', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseSerializer.self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='post':
          self.Meta.depth=0
        else:
          self.Meta.depth=1          

class StudentSummerySerializer(serializers.ModelSerializer):
    total_courses = serializers.SerializerMethodField()
    completed_courses = serializers.SerializerMethodField()
  
    class Meta:
        model = Teacher
        fields = '__all__'

class RateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = ['course', 'student', 'rating', 'review']



class EnrollmentRequestCreateSerializer(serializers.ModelSerializer):
    # student inferred from request.user (so client shouldn't set student)
    class Meta:
        model = EnrollmentRequest
        fields = ('request_id', 'course', 'payment_slip', 'status', 'created_at')
        read_only_fields = ('status', 'request_id', 'created_at')

    def validate_course(self, value):
        # Ensure course exists (DRF does that) and student's not already enrolled
        user = self.context['request'].user
        if EnrolledCourse.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        # ensure there is not already a pending request for same course
        if EnrollmentRequest.objects.filter(student=user, course=value, status=EnrollmentRequest.STATUS_PENDING).exists():
            raise serializers.ValidationError("You already have a pending enrollment request for this course.")
        return value

    def create(self, validated_data):
        student = self.context['request'].user
        validated_data['student'] = student
        enrollment_request = super().create(validated_data)
        return enrollment_request

class EnrollmentRequestListSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    teacher_name = serializers.CharField(source='course.teacher.full_name', read_only=True)

    class Meta:
        model = EnrollmentRequest
        fields = ('request_id', 'student', 'student_username', 'course', 'course_title', 'teacher_name',
                  'payment_slip', 'status', 'teacher_note', 'reviewed_by', 'created_at', 'updated_at')
        read_only_fields = ('status', 'teacher_note', 'reviewed_by', 'created_at', 'updated_at')

# api/serializers.py (append)



class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    # teacher is read-only: set in view from request.user -> Teacher
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'teacher', 'title', 'description',
            'image', 'price', 'language', 'level', 'platform_status',
            'course_id', 'slug', 'date'
        )
        read_only_fields = ('course_id', 'slug', 'date', 'teacher')

class CourseSerializer(serializers.ModelSerializer):
    teacher_full_name = serializers.CharField(source='teacher.full_name', read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('course_id', 'slug', 'date')

class CourseMaterialSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseMaterial
        fields = (
            'material_id', 'course', 'course_title', 'teacher',
            'title', 'description', 'video', 'pdf', 'image', 'note',
            'created_at', 'updated_at'
        )
        read_only_fields = ('material_id', 'teacher', 'created_at', 'updated_at')

    def validate(self, data):
        # ensure at least one of the content fields is provided
        if not (data.get('video') or data.get('pdf') or data.get('image') or (data.get('note') and data.get('note').strip())):
            raise serializers.ValidationError("Please provide at least one of: video, pdf, image, or note.")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        teacher = Teacher.objects.get(user=request.user)
        course = validated_data.get('course')
        # ensure teacher owns the course
        if course.teacher != teacher:
            raise serializers.ValidationError("You can only add materials to your own courses.")
        validated_data['teacher'] = teacher
        return super().create(validated_data)


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = '__all__'


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, read_only=True, source='quiz_answers')

    class Meta:
        model = QuizQuestion
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True, source='quiz_questions')

    class Meta:
        model = Quiz
        fields = '__all__'


class QuizQuestionAnswerSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'answers']

    def get_answers(self, obj):
        return [{'id': ans.id, 'answer_text': ans.answer_text} for ans in obj.quiz_answers.all()]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionAnswerSerializer(many=True, read_only=True, source='quiz_questions')

    class Meta:
        model = Quiz
        fields = ['quiz_id', 'title', 'description', 'questions']


class StudentQuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentQuizAnswer
        fields = ['question', 'selected_answer']


class StudentQuizAttemptSerializer(serializers.ModelSerializer):
    answers = StudentQuizAnswerSerializer(many=True)

    class Meta:
        model = StudentQuizAttempt
        fields = ['quiz', 'score', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        attempt = StudentQuizAttempt.objects.create(**validated_data)

        correct_count = 0
        for answer_data in answers_data:
            question = answer_data['question']
            selected_answer = answer_data['selected_answer']
            StudentQuizAnswer.objects.create(attempt=attempt, question=question, selected_answer=selected_answer)
            if selected_answer.is_correct:
                correct_count += 1

        # calculate score as percentage
        total_questions = len(answers_data)
        attempt.score = (correct_count / total_questions) * 100
        attempt.save()
        return attempt

