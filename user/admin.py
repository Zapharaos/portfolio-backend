from django.contrib import admin
from .models import (
    File, Technology, Project, ProjectTechnology, ProjectLink,
    Experience, ExperienceTechnology, WorkItem, Work, Hero, About, Footer, User, Social
)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_editable = ['color']


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectTechnologyInline, ProjectLinkInline]


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
