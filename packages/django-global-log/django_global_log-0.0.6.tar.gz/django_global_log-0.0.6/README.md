## Django Global Log

### 注册到 `installed_apps` 中

```python
INSTALLED_APPS = [
    "corsheaders",
    "django_global_log",
    ···
]
```

### 添加 `middleware`

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_global_log.middlewares.DjangoGlobalLogMiddleware",
    ···
]
```

### 使用 `celery`

```python
GLOBAL_LOG_CELERY_FUNC = "async_global_log"

def async_global_log(detail):
    DjangoGlobalLog.objects.create(**detail)
```
