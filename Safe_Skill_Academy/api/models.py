from django.db import models
from django.utils.text import slugify
from userauths.models import User, Profile  # if you use custom user model
from django.utils import timezone
from shortuuidfield import ShortUUIDField


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

    def students(self):
      return CartOrderItem.objects.filter(teacher=self)
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

