缓存
==
       由于Django是动态网站，所有每次请求均会去数据进行相应的操作，当程序访问量大时，耗时必然会更加明显，最简单解决方式是使用：缓存，缓存将一个某个views的返回值保存至内存或者memcache中，5分钟内再有人来访问时，则不再去执行view中的操作，而是直接从内存或者Redis中之前缓存的内容拿到，并返回。
       
中间件能做 csrftoken ,缓存,用户登录,权限系统

<b>缓存分为：</b>     
- 全站缓存（基于中间件实现）
- 局部视图函数缓存，给某个视图函数缓存（装饰器）
- 模板局部缓存
    
####Django中提供 缓存方式：      
```python     
- 开发调试
- 内存
- 文件
- 数据库
- Memcache缓存（python-memcached模块）
- Memcache缓存（pylibmc模块）
- Redis缓存
```    

####配置缓存settings.py文件    

<b>1.开发调试</b>    

```python     
# 此为开始调试用，实际内部不做任何操作    
    # 配置：
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',     # 引擎
                'TIMEOUT': 300,                                               # 缓存超时时间（默认300，None表示永不过期，0表示立即过期）
                'OPTIONS':{
                    'MAX_ENTRIES': 300,                                       # 最大缓存个数（默认300）
                    'CULL_FREQUENCY': 3,                                      # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
                },
                'KEY_PREFIX': '',                                             # 缓存key的前缀（默认空）
                'VERSION': 1,                                                 # 缓存key的版本（默认1）
                'KEY_FUNCTION' 函数名                                          # 生成key的函数（默认函数会生成为：【前缀:版本:key】）
            }
        }


    # 自定义key
    def default_key_func(key, key_prefix, version):
        """
        Default function to generate keys.

        Constructs the key used by all other methods. By default it prepends
        the `key_prefix'. KEY_FUNCTION can be used to specify an alternate
        function with custom key making behavior.
        """
        return '%s:%s:%s' % (key_prefix, version, key)

    def get_key_func(key_func):
        """
        Function to decide which key function to use.

        Defaults to ``default_key_func``.
        """
        if key_func is not None:
            if callable(key_func):
                return key_func
            else:
                return import_string(key_func)
        return default_key_func
```     

<b>2.本机内存</b>       
```python           
# 此缓存将内容保存至内存的变量中
    # 配置：
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }

    # 注：其他配置同开发调试版本
```     

<b>3.文件</b>       
```python           
# 此缓存将内容保存至文件
    # 配置：

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/django_cache',
            }
        }
    # 注：其他配置同开发调试版本
```       

<b>4.数据库</b>        
```python      
# 此缓存将内容保存至数据库
# 注：执行创建表命令 python manage.py createcachetable
    # 配置：
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'my_cache_table', # 数据库表
            }
        }
```       

<b>5.Memcache缓存（python-memcached模块）</b>        
```python         
# 此缓存使用python-memcached模块连接memcache

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/tmp/memcached.sock',
        }
    }   

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '172.19.26.240:11211',
                '172.19.26.242:11211',
            ]
        }
    }
```       

<b>6.Memcache缓存（pylibmc模块）</b>         
```python      
# 此缓存使用pylibmc模块连接memcache
    
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': '/tmp/memcached.sock',
        }
    }   

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': [
                '172.19.26.240:11211',
                '172.19.26.242:11211',
            ]
        }
    }
```       

<b>7.Redis 缓存（django-redis模块）</b>      
参考：http://django-redis-chs.readthedocs.io/zh_CN/latest/#redis
```python       
# 需要模块：
# pip install django-redis  
# yum install redis-server

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.1.20:6379/1",
        "TIMEOUT": 300,          # 默认超时时间
        'KEY_PREFIX': 'baolin',  # 缓存key的前缀（默认空）
        'VERSION': 3,            # 缓存key的版本（默认1）
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "password",    # 没有密码注释掉即可
            'MAX_ENTRIES': 5000,        # 最大缓存个数（默认300）
            'CULL_FREQUENCY': 3,       # 缓存到达最大个数之后，剔除缓存个数的比例，即：前 1/3（默认）会被删除掉
        }
    }
}

# 在redis中的格式：
# redis 127.0.0.1:8079[1]> KEYS *
# 1) "baolin:3:views.decorators.cache.cache_page..GET.146382e9a37a1da80e630eb042e9e924.d41d8cd98f00b204e9800998ecf8427e.en-us.UTC"
# 2) "baolin:3:views.decorators.cache.cache_header..146382e9a37a1da80e630eb042e9e924.en-us.UTC"
```       

#### 应用Django缓存 配置（全站 不可与 其他混用）      
<b>a. 全站使用（中间件）</b>       
```python      
# 使用中间件，经过一系列的认证等操作，如果内容在缓存中存在，则使用FetchFromCacheMiddleware获取内容并返回给用户，当返回给用户之前，判断缓存中是否已经存在，如果不存在则UpdateCacheMiddleware会将缓存保存至缓存，从而实现全站缓存

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # 开头
    # 其他中间件...
    # 结尾
    'django.middleware.cache.FetchFromCacheMiddleware',
]
```      

<b>b.局部视图函数缓存，给某个视图函数缓存（装饰器）</b>       
```python         
# 方式一(在视图函数中引用)：

from django.views.decorators.cache import cache_page
# 超时时间(秒) 15分钟
@cache_page(60 * 15)
def users(request):
    ctime = str(time.time())
    print(ctime)
    return HttpResponse(ctime)


# 方式二（在路由中引用urls）：
from django.views.decorators.cache import cache_page

from app01 import views
urlpatterns = [
    url(r'^users/', cache_page(60 * 15)(views.users)),
]
```        

<b>c.模板局部缓存(在template模板中引用)</b>       
```python           
# 引用 TemplateTag
{% load cache %}

# 使用方式
<body>
    <h1>{{ ctime }}</h1>

    {% cache 300 keyname %}    {# 300 为时间 秒；keyname 可以标记 该缓存的内容标记 #}
        <a style="color: red">{{ ctime }}</a>
    {% endcache %}
</body>

# 在redis中的格式：
# redis 127.0.0.1:8079[1]> KEYS *
# 1) "baolin:3:template.cache.keyname.d41d8cd98f00b204e9800998ecf8427e"
```        