import os

from django import forms
from django.contrib import admin
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Q
from django.utils.html import format_html
from .models import (
    File, Technology, Project, ProjectTechnology, ProjectLink,
    Experience, ExperienceTechnology, WorkItem, Work, Hero, About, Footer, Theme, User, Social
)


class FileAdminForm(forms.ModelForm):
    class Meta:
        model = File
        fields = '__all__'

    def clean_file(self):
        """Warn (block) when the uploaded file name is already used by another
        File record — uploading it would overwrite that file (OverwriteStorage)."""
        uploaded = self.cleaned_data.get('file')
        # Only check a freshly uploaded file, not an unchanged existing one.
        if not isinstance(uploaded, UploadedFile):
            return uploaded

        name = os.path.basename(uploaded.name)
        clash = (
            File.objects
            .exclude(pk=self.instance.pk)
            .filter(Q(file=name) | Q(file__endswith='/' + name))
            .first()
        )
        if clash:
            raise forms.ValidationError(
                f'A file named "{name}" is already used by "{clash.name}" (id {clash.pk}). '
                f'Uploading it would overwrite that file. Rename your file, or edit that '
                f'record instead.'
            )
        return uploaded


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    form = FileAdminForm
    list_display = ['name', 'file']
    search_fields = ['name', 'file']


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
    list_display = ['title', 'index', 'hidden', 'healthUp', 'healthCheckedAt', 'healthFailures']
    # Editable straight from the list for quick reordering / (un)hiding.
    list_editable = ['index', 'hidden']
    # Sorted by index by default; click the "index" column header to toggle.
    ordering = ['index']
    list_filter = ['hidden']
    readonly_fields = ['healthUp', 'healthCheckedAt', 'healthFailures']


class ExperienceTechnologyInline(admin.TabularInline):
    model = ExperienceTechnology
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [ExperienceTechnologyInline]


admin.site.register(WorkItem)
admin.site.register(Work)
admin.site.register(Hero)
admin.site.register(About)
admin.site.register(Footer)
admin.site.register(User)
admin.site.register(Social)
