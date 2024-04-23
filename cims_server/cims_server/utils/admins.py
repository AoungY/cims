from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):

    # 对删除操作进行修改,改为逻辑删除
    # def delete_queryset(self, request, queryset):
    #     for i in queryset:
    #         i.is_delete = 1
    #         i.save()

    # 对查询操作进行筛选,is_delete为True的不显示
    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     return queryset.filter(is_delete=False)
    pass