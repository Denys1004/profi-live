from django.contrib import admin
from .models import *
# Register your models here.
class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, JobAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, JobAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, JobAdmin)