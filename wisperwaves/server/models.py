from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Model representing a category.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the Category instance.
        """
        return self.name

class Server(models.Model):
    """
    Model representing a server.
    """
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='servers_owner'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='server_category'
    )
    description = models.CharField(max_length=250, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        """
        String representation of the Server instance.
        """
        return self.name

class Channel(models.Model):
    """
    Model representing a channel.
    """
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")

    def save(self, *args, **kwargs):
        """
        Override the save method to convert the channel name to lowercase before saving.
        """
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Channel instance.
        """
        return self.name
