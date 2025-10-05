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
    course_id=ShortUUIDField(length=6, max_length=20, prefix="CRS", alphabet="1234567890", unique=True, editable=False)
    slug = models.SlugField(unique=True)
    date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug =='' or self.slug == None:
            self.slug = slugify(self.title)
        super(Category,self).save(*args, **kwargs)
