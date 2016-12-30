from django.db import models


class RemoteHost(models.Model):
    ip_address = models.CharField(max_length=16, unique=True)
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    geo_location = models.CharField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{0}({1})".format(self.ip_address, self.domain_name)


class SearchEngine(models.Model):
    name = models.CharField(max_length=64)
    referer_url = models.CharField(max_length=255)
    doc_page = models.CharField(max_length=255)


class UserAgent(models.Model):
    DEVICE_TYPE = (
        ('C', 'Computers'),
        ('P', 'Phones'),
        ('T', 'Tablets')
    )
    operating_system = models.CharField(max_length=64)
    browser = models.CharField(max_length=64)
    device_type = models.CharField(max_length=1, choices=DEVICE_TYPE, blank=True, null=True)
    search_engine = models.ForeignKey(SearchEngine, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{0}:{1}".format(self.operating_system, self.browser)


class RequestedUri(models.Model):
    uri = models.CharField(max_length=1024, unique=True)
    visit_count = models.IntegerField(default=0)
    should_crawl = models.BooleanField()

    def __str__(self):
        return self.uri


class Referer(models.Model):
    url = models.CharField(max_length=1024, unique=True)
    internal_uri = models.ForeignKey(RequestedUri, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class LogEntry(models.Model):
    timestamp = models.IntegerField()
    remote_host = models.ForeignKey(RemoteHost, on_delete=models.CASCADE)
    requested_uri = models.ForeignKey(RequestedUri, on_delete=models.CASCADE)
    referer = models.ForeignKey(Referer, on_delete=models.CASCADE)
    user_agent = models.ForeignKey(UserAgent, on_delete=models.CASCADE)
    status_code = models.IntegerField()
    method = models.CharField(max_length=16)


class IgnoredUri(models.Model):
    pattern = models.CharField(max_length=512)


class IgnoredHost(models.Model):
    host = models.ForeignKey(RemoteHost, on_delete=models.CASCADE)
    reason = models.CharField(max_length=1024)


class CacheableParam(models.Model):
    param = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
