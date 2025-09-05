from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.snippets.models import register_snippet

from slugify import slugify

from wagtail.search import index

from wagtail.api import APIField
from rest_framework.fields import DateField, CharField
from wagtail.rich_text import expand_db_html

class RichTextSerializer(CharField):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return expand_db_html(representation)

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + ["intro"]

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    # Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            "date", 
            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
            "tags"  
        ], 
        heading="Blog information"),
        "intro", "body", "gallery_images"
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # Export fields over the API
    api_fields = [
        APIField('intro'),
        APIField('date'),
        APIField('date_display', serializer=DateField(format='%A %d %B %Y', source='date')),
        APIField('body', serializer=RichTextSerializer()),
        APIField('intro'),
        APIField('authors'),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]    

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = 'Authors'

    api_fields = [
        APIField('name'),
    ]

class BlogTagIndexPage(Page):
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context