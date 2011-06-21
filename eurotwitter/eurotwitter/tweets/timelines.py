from nydus.db import create_cluster

class Timeline(object):
    def __init__(self, model, name):
        self.redis = create_cluster({
            'engine': 'nydus.db.backends.redis.Redis',
            'router': 'nydus.db.routers.redis.PartitionRouter',
            'hosts': dict((n, {'db': n}) for n in xrange(9)),
        })
        self.model = model
        self.ns = 'timeline:%s' % name

    def add(self, instance, **kwargs):
        self.redis.zadd(self.get_key(**kwargs), instance.id, float(instance.date.strftime('%s.%m')))

    def remove(self, instance, **kwargs):
        self.redis.zrem(self.get_key(**kwargs), instance.id)
    
    def list(self, offset=0, limit=-1, **kwargs):
        id_list = self.redis.zrevrange(self.get_key(**kwargs), offset, limit)
        obj_cache = dict((t.pk, t) for t in self.model.objects.filter(pk__in=id_list))

        results = filter(None, [obj_cache.get(t) for t in id_list])

        return results
    
    def flush(self, **kwargs):
        self.redis.delete(self.get_key(**kwargs))

    def get_key(self, **kwargs):
        kwarg_str = '&'.join('%s=%s' % (k, v) for k, v in sorted(kwargs.items()))
        
        return '%s:%s' % (self.ns, kwarg_str)
