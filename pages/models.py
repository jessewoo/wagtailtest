from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail.blocks import (
    CharBlock, RichTextBlock, StreamBlock, StructBlock,
    TextBlock, URLBlock, PageChooserBlock, ListBlock
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search import index
from wagtail.api import APIField
from modelcluster.fields import ParentalKey


class StandardPage(Page):
    """Generic content pages (About, Privacy, etc.)"""

    intro = models.TextField(
        blank=True,
        help_text="Optional introduction text"
    )

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Optional header image"
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('header_image'),
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    api_fields = [
        APIField('intro'),
        APIField('body'),
        APIField('header_image'),
    ]

    class Meta:
        verbose_name = "Standard Page"


class AboutPage(Page):
    """Company/organization info with mission/vision"""

    intro = RichTextField(
        blank=True,
        help_text="Introduction about the organization"
    )

    mission = RichTextField(
        blank=True,
        help_text="Mission statement"
    )

    vision = RichTextField(
        blank=True,
        help_text="Vision statement"
    )

    body = RichTextField(
        blank=True,
        help_text="Additional content"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('mission'),
            FieldPanel('vision'),
        ], heading="Mission & Vision"),
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('mission'),
        index.SearchField('vision'),
        index.SearchField('body'),
    ]

    api_fields = [
        APIField('intro'),
        APIField('mission'),
        APIField('vision'),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "About Page"


class ServicesPage(Page):
    """Parent page for service listings"""

    intro = RichTextField(
        blank=True,
        help_text="Introduction to services"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['pages.ServicePage']

    api_fields = [
        APIField('intro'),
    ]

    class Meta:
        verbose_name = "Services Page"


class ServicePage(Page):
    """Individual service details"""

    description = RichTextField(
        blank=True,
        help_text="Service description"
    )

    features = RichTextField(
        blank=True,
        help_text="Key features or benefits"
    )

    pricing_info = models.CharField(
        max_length=255,
        blank=True,
        help_text="Pricing information"
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('features'),
        FieldPanel('pricing_info'),
    ]

    parent_page_types = ['pages.ServicesPage']

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('features'),
    ]

    api_fields = [
        APIField('description'),
        APIField('features'),
        APIField('pricing_info'),
    ]

    class Meta:
        verbose_name = "Service Page"


class ContactPage(Page):
    """Contact info with social media links"""

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    body = RichTextField(
        blank=True,
        help_text="Additional contact information"
    )

    facebook_url = models.URLField(
        blank=True,
        verbose_name="Facebook URL"
    )

    twitter_url = models.URLField(
        blank=True,
        verbose_name="Twitter/X URL"
    )

    linkedin_url = models.URLField(
        blank=True,
        verbose_name="LinkedIn URL"
    )

    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram URL"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('address'),
        ], heading="Contact Information"),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('twitter_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('instagram_url'),
        ], heading="Social Media Links"),
    ]

    api_fields = [
        APIField('phone'),
        APIField('email'),
        APIField('address'),
        APIField('body'),
        APIField('facebook_url'),
        APIField('twitter_url'),
        APIField('linkedin_url'),
        APIField('instagram_url'),
    ]

    class Meta:
        verbose_name = "Contact Page"


class FAQItem(models.Model):
    """Individual FAQ question and answer"""

    page = ParentalKey(
        'FAQPage',
        on_delete=models.CASCADE,
        related_name='faq_items'
    )

    question = models.CharField(max_length=255)
    answer = RichTextField()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"


class FAQPage(Page):
    """Frequently asked questions with inline Q&A"""

    intro = RichTextField(
        blank=True,
        help_text="Introduction to FAQs"
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('faq_items', label="FAQ Items"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]

    api_fields = [
        APIField('intro'),
        APIField('faq_items'),
    ]

    class Meta:
        verbose_name = "FAQ Page"


class FlexibleContentBlock(StreamBlock):
    """Most flexible content block for building custom page layouts"""

    heading = CharBlock(
        max_length=255,
        classname="title",
        icon="title"
    )

    paragraph = RichTextBlock(
        icon="pilcrow"
    )

    image = ImageChooserBlock(
        icon="image"
    )

    embed = EmbedBlock(
        icon="media"
    )

    document = DocumentChooserBlock(
        icon="doc-full-inverse"
    )

    call_to_action = StructBlock([
        ('title', CharBlock(max_length=255)),
        ('text', RichTextBlock()),
        ('button_text', CharBlock(max_length=50)),
        ('button_link', URLBlock(required=False)),
        ('button_page', PageChooserBlock(required=False)),
    ], icon="plus-inverse")

    quote = StructBlock([
        ('text', TextBlock()),
        ('author', CharBlock(max_length=100, required=False)),
        ('author_title', CharBlock(max_length=100, required=False)),
    ], icon="openquote")

    columns = StructBlock([
        ('columns', ListBlock(StructBlock([
            ('heading', CharBlock(max_length=255, required=False)),
            ('content', RichTextBlock()),
        ]))),
    ], icon="grip")

    anchor = CharBlock(
        max_length=100,
        help_text="Add an anchor/ID for linking to this section",
        icon="link"
    )

    class Meta:
        icon = "placeholder"


class FlexiblePage(Page):
    """Advanced page with StreamField blocks"""

    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional subtitle for the page"
    )

    body = StreamField(
        FlexibleContentBlock(),
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
    ]

    api_fields = [
        APIField('subtitle'),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "Flexible Page"
