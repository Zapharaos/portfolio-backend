from django.contrib import admin
from .models import User, Social, List, ListItem, Theme, Footer, SVG

admin.site.register(Theme)
admin.site.register(User)
admin.site.register(Social)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Footer)
admin.site.register(SVG)
