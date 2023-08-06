import time
from functools import wraps
from om_helper.helper import run


def run_decorator(onerror=None, onsuccess=None):
    def inner(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)
                if callable(onsuccess):
                    return onsuccess(ret)
                return ret
            except Exception as e:
                if callable(onerror):
                    return onerror(e)
                raise e

        return _inner

    return inner


def retry_decorator(times=0, interval=0, onerror=None, onretry=None, onsuccess=None):
    def _retry(f, _times, *args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            if callable(onsuccess):
                return run(onsuccess, ret, onerror=lambda e: None)
            return ret
        except Exception as exc:
            if _times > 0:
                if callable(onretry):
                    return run(onretry, exc=exc, onerror=lambda e: None)
                if interval > 0:
                    time.sleep(interval)
                return _retry(f, _times - 1, *args, **kwargs)
            if callable(onerror):
                return run(onerror, exc=exc, onerror=lambda e: None)
            raise exc

    def inner(f):
        @wraps(f)
        def _inner(*args, **kwargs):
            return _retry(f, times, *args, **kwargs)

        return _inner

    return inner
