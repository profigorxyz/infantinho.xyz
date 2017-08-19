from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
# from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID


class PostManager(models.Manager):
    """docstring for PostManager"""

    def active(self, *args, **kwargs):
        return super(PostManager, self).\
            filter(draft=False).\
            filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    if instance.pk:
        instpk = instance.pk
    else:
        instpk = 'upload'
    return 'media/blog/{}/{}'.format(instpk, filename)


class Post(models.Model):
    """docstring for Post"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1)
    title = models.CharField(max_length=120,
                             verbose_name='título')
    slug = models.SlugField(unique=True)
    headimage = StdImageField(null=True,
                              blank=True,
                              upload_to=UploadToUUID(upload_location),
                              verbose_name='imagem de destaque',
                              variations={
                                  'large': (1920, 1280),
                                  'thumbnail': (100, 100, True),
                                  'medium': (800, 600),
                                  'small': (400, 300)
                              })
    content = models.TextField(verbose_name='conteúdo')
    tag = models.CharField(max_length=40,
                           default="TIC")
    draft = models.BooleanField(default=False,
                                verbose_name='rascunho')
    publish = models.DateField(auto_now=False,
                               auto_now_add=False,
                               default=timezone.now,
                               verbose_name='publicado em')
    updated = models.DateTimeField(auto_now=True,
                                   auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,
                                     auto_now_add=True)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('blog:edit', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-publish', '-timestamp', '-updated']

    # @property
    # def comments(self):
    #     instance = self
    #     qs = Comment.objects.filter_by_instance(instance)
    #     return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '{}-{}'.format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
