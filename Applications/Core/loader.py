from django.core.cache import cache


class CacheLoader:
    
    def load_cache(self,kwargs):
        kwargs["channel"]= cache.get("channel")
        kwargs["channelcontent"]=cache.get("channelcontent")
        
        return kwargs