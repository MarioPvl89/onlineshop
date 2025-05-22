from django.contrib import admin
from .models import Comment, Categories, Products


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_text', 'product', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('user__username', 'text', 'product__name')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Комментарий'


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'price', 'discount', 'quantity')
    search_fields = ('name',)


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name',)
    search_fields = ('name',)
