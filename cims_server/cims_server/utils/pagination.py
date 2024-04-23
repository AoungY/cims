from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """自定义分页类"""
    page_size = 20  # 指定默认每页显示多少条数据
    max_page_size = 50  # 每页最大显示多少条数据
    page_size_query_param = 'limit'  # 前端用来指定每页显示第几页 查询关键字 默认就是page_size

    def get_paginated_response(self, data):
        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },

            'total': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
