from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField

# keep the definition of BlogIndexPage model, and add the BlogPage model:

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["date", "intro", "body"]