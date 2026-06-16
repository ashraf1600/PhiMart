from django.contrib import admin
from .models import Product, Category, Review, ProductImage  # Import ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Show 3 empty fields for adding multiple images
    fields = ['image', 'alt_text']
    max_num = 10  # Maximum 10 images per product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'category', 'created_at']
    list_filter = ['category', 'created_at', 'stock']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    inlines = [ProductImageInline]  # This is crucial for uploading images inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'product_count']
    search_fields = ['name']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Product Count'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'ratings', 'comment_preview', 'created_at']
    list_filter = ['ratings', 'created_at']
    search_fields = ['product__name', 'user__email', 'comment']

    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment Preview'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_preview', 'alt_text']
    list_filter = ['product']

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover;" />'
        return 'No Image'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'