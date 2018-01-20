from django.db import models

class Configuration(models.Model):
    invalid_user_message = models.CharField(max_length=100)
    invalid_password_message = models.CharField(max_length=100)
    new_user_exists_rate = models.IntegerField(blank=False, default=20)

    def __str__(self):
        return 'Application Configuration Options'


class AttemptUser(models.Model):
    username = models.CharField(max_length=100, blank=False)
    exists = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    
class AttemptSource(models.Model):
    credentials = models.ForeignKey(AttemptUser, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(protocol='IPv4', blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip
