from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


def category_icon_upload_path(instance,filename):
    return f"category/{instance.id}/category_icon/{filename}"

class Category(models.Model):
    """
    Model representing a category.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category,id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            super(Category,self).save(*args, **kwargs)
            
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender,instance,**kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                if getattr(instance,field.name):
                    getattr(instance,field.name).delete(save=False)
                    
                    
    def __str__(self) -> str:
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
