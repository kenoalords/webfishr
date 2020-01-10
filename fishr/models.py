from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=24)
    slug = models.SlugField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Package(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    regular_price = models.IntegerField(blank=True)
    sale_price = models.IntegerField()
    position = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    features = models.ManyToManyField('Feature')
    image = models.ImageField(upload_to='packages', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s N%s - %s' % (self.title, self.sale_price, self.category.title)

    class Meta:
        ordering = ['position']

class Feature(models.Model):
    title = models.CharField(max_length=64)
    def __str__(self):
        return self.title

class Theme(models.Model):
    title = models.CharField(max_length=32)
    image = models.ImageField(upload_to="themes")
    slug = models.SlugField(max_length=32, blank=True)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('design', kwargs={ 'slug': self.slug })

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True)
    domain_name = models.URLField(blank=True)
    amount = models.FloatField()
    amount_paid = models.FloatField(null=True)
    transaction_ref = models.CharField(max_length=1024, blank=True)
    payment_type = models.CharField(choices=(('online', 'Online Payment'), ('transfer', 'Bank Transfer')), max_length=12)
    is_paid = models.BooleanField(default=False)
    is_service_active = models.BooleanField(default=False)
    expiry = models.DateField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user.first_name, self.package.title)

    def get_absolute_url(self):
        return reverse('order', kwargs={ 'uuid': self.uuid })

    class Meta:
        ordering = ['-date']

class Product(models.Model):
    uuid = models.UUIDField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

class Testimonial(models.Model):
    name = models.CharField(max_length=32)
    title = models.CharField(max_length=32, blank=True)
    testimonial = models.CharField(max_length=256)
    avatar = models.ImageField(upload_to="avatar")
    order = models.IntegerField(default=10)
    is_visible = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Faq(models.Model):
    question = models.CharField(max_length=128)
    answer = models.CharField(max_length=1024)
    order = models.IntegerField(default=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.question, self.order)

    class Meta:
        ordering = ['order']


class EmailSubscription(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    is_verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']


class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class PollOptions(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.CharField(max_length=128)
    votes = models.IntegerField()




# End ---
