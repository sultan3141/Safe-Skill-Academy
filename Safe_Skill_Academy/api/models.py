from django.db import models
from django.utils.text import slugify
from users.models import User, Profile  # if you use custom user model
from django.utils import timezone
from shortuuidfield import ShortUUIDField
from django.db import transaction
from django.core.exceptions import ValidationError
import uuid

language=(("English","English"),("Amharic","Amharic"),("Oromifa","Oromifa"),)
Level=(("Beginner","Beginner"),("Intermediate","Intermediate"),("Advanced","Advanced"),)
Platform_Status=(("Free","Free"),("Paid","Paid"),)

class Teacher(models.Model):  # example model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='teachers/')
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    facebook = models.URLField(blank=True, null=True)
    x= models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name
    def courses(self):
      return Course.objects.filter(teacher=self)
    def reviews(self):
      return Course.objects.filter(teacher=self).count()
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/')
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

    def course_count(self):
        return self.courses.count()  # 'courses' is the related_name in Course model's ForeignKey

    def save(self, *args, **kwargs):
        if self.slug =='' or self.slug == None:
            self.slug = slugify(self.title)
        super(Category,self).save(*args, **kwargs)        


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course-file')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    language = models.CharField(max_length=50, choices=language, default="English")
    level = models.CharField(max_length=50, choices=Level, default="Beginner")
    platform_status = models.CharField(max_length=50, choices=Platform_Status, default="Free")
    course_id = ShortUUIDField(
        max_length=22,  # default length
        unique=True,
        editable=False
    )
    slug = models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug =='' or self.slug == None:
            self.slug = slugify(self.title)
        super(Category,self).save(*args, **kwargs)
    def students(self):
      return EnrolledCourse.objects.filter(course=self)

    def curriculum(self):
      return VariantItem.objects.filter(course=self)

    def lactures(self):
      return VariantItem.objects.filter(course=self)

    def average_rating(self):
       average_rating=Review.objects.filter(course=self).aggregate(avg_rating=models.AVG('rating'))
       return average_rating['avg_rating']

    def rating_count(self):
       return Review.objects.filter(course=self, active=True).count()  

    def reviews(self):
       return Review.objects.filter(course=self, active=True)

class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    variant_id=ShortUUIDField(max_length=20, unique=True, editable=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def Variant_items(self):
          return VariantItem.objects.filter(variant=self)


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='course_materials/videos/', null=True, blank=True)
    pdf = models.FileField(upload_to='course_materials/pdfs/', null=True, blank=True)
    image = models.ImageField(upload_to='course_materials/images/', null=True, blank=True)
    note = models.TextField(blank=True, null=True)  # textual note/summary
    material_id = ShortUUIDField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    def clean(self):
        # ensure material.teacher matches course.teacher
        if self.teacher and self.course and self.teacher != self.course.teacher:
            raise ValidationError("Material teacher must be the same as the course teacher.")
        # ensure at least one attachment or note
        if not (self.video or self.pdf or self.image or (self.note and self.note.strip())):
            raise ValidationError("Provide at least one of: video, pdf, image or note.")


class VariantItem(models.Model):
    variant = models.ForeignKey("Variant", on_delete=models.CASCADE)
    file = models.FileField(upload_to="course-file")
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_duration = models.DurationField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(
        max_length=20, unique=True, editable=False
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    qa_id=ShortUUIDField(max_length=20, unique=True, editable=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.user.username} - {self.course.title}"

    class Meta:
        ordering = ['-date'] 

    def massages(self):
      return Question_Answer_Massage.objects.filter(question=self)  
    def Profile(self):
      return Profile.objects.get(user=self.user)

class Question_Answer_Massage(models.Model):
     course=models.ForeignKey(Course, on_delete=models.CASCADE)
     question=models.ForeignKey(Question_Answer, on_delete=models.CASCADE)
     user=models.ForeignKey(User, on_delete=models.CASCADE)
     massage=models.TextField()
     qam_id=ShortUUIDField(max_length=20, unique=True, editable=False)
     date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"{ self.user.username} - {self.course.title}"

     class Meta:
        ordering = ['date']   

     def Profile(self):
        return Profile.objects.get(user=self.user)  
class CompletedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.title

class EnrolledCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)  # percentage of course completed
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    enrolled_id=ShortUUIDField(max_length=20, unique=True, editable=False)

    def __str__(self):
        return self.course.title

    def lectures(self):
      return VariantItem.objects.filter(variant_course=self.course)
    
    def completed_lectures(self):
      return CompletedLecture.objects.filter(user=self.user, course=self.course)
    
    def curriculum(self):
      return VariantItem.objects.filter(course=self.course)

    def note(self):
      return Note.objects.filter(user=self.user, course=self.course) 

    def review(self):
      return Review.objects.filter(user=self.user, course=self.course).frist()

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note_id=ShortUUIDField(max_length=20, unique=True, editable=False)  

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review=models.CharField(max_length=200)
    rating = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_id=ShortUUIDField(max_length=20, unique=True, editable=False)  

    def __str__(self):
        return self.review

    def Profile(self):
      return Profile.objects.get(user=self.user)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    review=models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.user        

class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # e.g., 1 to 5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')  # one rating per student per course

    def __str__(self):
        return f"{self.student} rated {self.course} - {self.rating}"
        
class country(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# reuse existing User, Course, Teacher, EnrolledCourse imports you already have
# from userauths.models import User
# from .models import Course, Teacher, EnrolledCourse  # these already exist in the file

class EnrollmentRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='enrollment_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_requests')
    payment_slip = models.ImageField(upload_to='enrollment_slips/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    teacher_note = models.TextField(blank=True, null=True)  # optional note from teacher (reason for rejection etc)
    reviewed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_enrollment_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    request_id = ShortUUIDField(max_length=20, unique=True, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} -> {self.course.title} ({self.status})"

    def approve(self, reviewer: Teacher):
        """
        Approve this request and create EnrolledCourse if not already enrolled.
        """
        if self.status == self.STATUS_APPROVED:
            return

        with transaction.atomic():
            # mark approved
            self.status = self.STATUS_APPROVED
            self.reviewed_by = reviewer
            self.updated_at = timezone.now()
            self.save(update_fields=['status', 'reviewed_by', 'updated_at'])

            # create enrolled course if not exists
            enrolled, created = EnrolledCourse.objects.get_or_create(
                user=self.student,
                course=self.course,
                defaults={'teacher': self.course.teacher}
            )
            return enrolled, created

    def reject(self, reviewer: Teacher, note: str = None):
        self.status = self.STATUS_REJECTED
        self.reviewed_by = reviewer
        if note:
            self.teacher_note = note
        self.updated_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_by', 'teacher_note', 'updated_at'])

class Quiz(models.Model):
    quiz_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_quizzes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class QuizQuestion(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TF', 'True / False'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES, default='MCQ')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_text} ({self.get_question_type_display()})"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='quiz_answers')
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text} ({'correct' if self.is_correct else 'wrong'})"


class StudentQuizAttempt(models.Model):
    attempt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} - {self.score}"


class StudentQuizAnswer(models.Model):
    attempt = models.ForeignKey(StudentQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attempt.student.username} - {self.question.question_text}"
