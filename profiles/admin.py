from django.contrib import admin
from .models import User, Portfolio, Social, List, ListItem, Theme, DefaultUser

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(Social)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Theme)
admin.site.register(DefaultUser)
