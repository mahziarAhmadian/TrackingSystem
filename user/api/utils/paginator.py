class CustomPaginator:
    def __init__(self, page=1, count=10):
        self.page = page
        self.count = count

    def pagination_query(self, query_object, order_by_object):
        offset = int((self.page - 1) * self.count)
        limit = int(self.count)
        pagination_query = query_object.order_by(order_by_object)[offset:offset + limit]
        return pagination_query
