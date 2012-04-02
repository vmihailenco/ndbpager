import hashlib

from google.appengine.api import memcache
from google.appengine.datastore.datastore_query import Cursor


__all__ = ['Pager']


class BasePager(object):
    def __init__(self, **kwargs):
        try:
            self.page = int(kwargs.pop('page', 1))
        except ValueError:
            self.page = 1
        if self.page < 1:
            self.page = 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def prev_page(self):
        if self.has_prev:
            return self.page - 1
        else:
            return self.page

    @property
    def next_page(self):
        if self.has_next:
            return self.page + 1
        else:
            return self.page

    def __nonzero__(self):
        return self.has_prev or self.has_next


class Pager(BasePager):
    def __init__(self, **kwargs):
        self.query = kwargs.pop('query')
        self.lifetime = kwargs.pop('lifetime', 3600)
        super(Pager, self).__init__(**kwargs)

    def paginate(self, page_size=20, **q_options):
        if self.page > 1:
            cursor, more = self._get_from_cache(self.page - 1)
            if not cursor:
                self.page, cursor, _ = self._get_max_avail_page(page_size)
        else:
            cursor = None

        res, cursor, more = self._fetch_page(
            page_size, start_cursor=cursor, **q_options)
        if cursor:
            self._add_to_cache(self.page, cursor, more)
        self.has_next = more

        return res, cursor, more

    def _fetch_page(self, *args, **q_options):
        return self.query.fetch_page(*args, **q_options)

    @property
    def _query_id(self):
        if not hasattr(self, '__query_id'):
            hsh = hashlib.md5()
            hsh.update(repr(self.query))
            self.__query_id = hsh.hexdigest()
        return self.__query_id

    def _get_cache_key(self, page):
        return '%s%s' % (self._query_id, page)

    def _add_to_cache(self, page, cursor, more):
        value = cursor.to_bytes() + str(int(more))
        memcache.set(
            self._get_cache_key(page),
            value,
            namespace=self.__class__.__name__)

    def _get_from_cache(self, page):
        value = memcache.get(
            self._get_cache_key(page), namespace=self.__class__.__name__)
        if not value:
            return None, None
        cursor = Cursor.from_bytes(value[:-1])
        more = bool(int(value[-1:]))
        return cursor, more

    def _get_max_avail_page(self, page_size):
        # set limit to 1000 results to prevent abuse
        prev_cursor = None
        for page in xrange(1, 1000 / page_size):
            cursor, more = self._get_from_cache(page)
            if not cursor:
                res, cursor, more = self._fetch_page(
                    page_size, start_cursor=prev_cursor, keys_only=True)
                if cursor:
                    self._add_to_cache(page, cursor, more)
            if not more:
                return page, prev_cursor, more
            prev_cursor = cursor
        else:
            return page, cursor, more
