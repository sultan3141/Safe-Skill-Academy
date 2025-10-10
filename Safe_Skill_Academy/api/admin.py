from django.contrib import admin
from .models import (
    Teacher, Category, Course, Variant, VariantItem,
    Question_Answer, Question_Answer_Massage,
    CompletedCourse, EnrolledCourse, Note, Review,
    Notification, country,CourseMaterial, Quiz, QuizQuestion, QuizAnswer, StudentQuizAttempt, StudentQuizAnswer
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'country']
    search_fields = ['full_name', 'user__username']
    prepopulated_fields = {'slug': ('full_name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'category', 'price', 'language', 'level', 'platform_status']
    search_fields = ['title', 'teacher__full_name']
    list_filter = ['language', 'level', 'platform_status']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'date']
    search_fields = ['title', 'course__title']

@admin.register(VariantItem)
class VariantItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'variant', 'preview', 'date']
    search_fields = ['title', 'variant__title']
    list_filter = ['preview']

@admin.register(Question_Answer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'course', 'date']
    search_fields = ['title', 'user__username', 'course__title']
    ordering = ['-date']

@admin.register(Question_Answer_Massage)
class QuestionAnswerMassageAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'question', 'date']
    search_fields = ['user__username', 'course__title']
    ordering = ['date']

@admin.register(CompletedCourse)
class CompletedCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completed_at']
    search_fields = ['user__username', 'course__title']

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'teacher', 'progress', 'enrolled_at']
    search_fields = ['user__username', 'course__title', 'teacher__full_name']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'course', 'created_at']
    search_fields = ['title', 'user__username', 'course__title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'course', 'rating', 'active', 'created_at']
    search_fields = ['review', 'user__username', 'course__title']
    list_filter = ['active', 'rating']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'is_read', 'created_at']
    search_fields = ['user__username', 'type']
    list_filter = ['is_read']

@admin.register(country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    search_fields = ['name']
    list_filter = ['active']

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'teacher', 'created_at', 'updated_at']
    search_fields = ['title', 'course__title', 'teacher__full_name']
    list_filter = ['created_at', 'teacher']
    readonly_fields = ['material_id', 'created_at', 'updated_at']


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'created_at')
    inlines = [QuizQuestionInline]

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'created_at')
    inlines = [QuizAnswerInline]

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'question', 'is_correct')

# Student quiz attempts
class StudentQuizAnswerInline(admin.TabularInline):
    model = StudentQuizAnswer
    extra = 0

@admin.register(StudentQuizAttempt)
class StudentQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'submitted_at')
    inlines = [StudentQuizAnswerInline]

@admin.register(StudentQuizAnswer)
class StudentQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_answer')
