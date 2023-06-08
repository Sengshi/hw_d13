from django.contrib import admin

from .models import Post, Category, Retry


class CategoryAdm(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_filter = ('category', )
    search_fields = ('category',)


admin.site.register(Post)
admin.site.register(Category, CategoryAdm)
# admin.site.register(PostRetry)
admin.site.register(Retry)
