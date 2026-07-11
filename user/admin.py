from django.contrib import admin
from django.utils.html import format_html
from .models import (
    File, Technology, Project, ProjectTechnology, ProjectLink,
    Experience, ExperienceTechnology, WorkItem, Work, Hero, About, Footer, Theme, User, Social
)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_editable = ['color']


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'background', 'text', 'primary', 'preview']

    @admin.display(description='Preview')
    def preview(self, obj):
        swatch = (
            '<span style="display:inline-block;width:16px;height:16px;'
            'border:1px solid #888;border-radius:3px;background:{};"></span>'
        )
        return format_html(
            '<span style="display:inline-flex;gap:4px;">' + swatch * 3 + '</span>',
            obj.background, obj.text, obj.primary,
        )


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectTechnologyInline, ProjectLinkInline]
    list_display = ['title', 'healthUp', 'healthCheckedAt', 'healthFailures']
    readonly_fields = ['healthUp', 'healthCheckedAt', 'healthFailures']


class ExperienceTechnologyInline(admin.TabularInline):
    model = ExperienceTechnology
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [ExperienceTechnologyInline]


admin.site.register(File)
admin.site.register(WorkItem)
admin.site.register(Work)
admin.site.register(Hero)
admin.site.register(About)
admin.site.register(Footer)
admin.site.register(User)
admin.site.register(Social)
