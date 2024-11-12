from django.db import models

# Create your models here.



from django.db import models

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')

class customertbl(models.Model):
    nam = models.CharField(max_length=100)
    cnum = models.CharField(max_length=100)
    eml = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default='website')
    uname = models.CharField(max_length=100)
    is_pending_approval = models.BooleanField(default=False,blank=True,null=True)  # Add this field
    is_approved = models.BooleanField(default=False)  # Not approved by default


    def __str__(self):
        return self.nam



class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    session_key = models.CharField(max_length=100, blank=True, null=True)  # Add this field

    def __str__(self):
        return self.username



    
class UploadedVideo(models.Model):
    video_file = models.FileField(upload_to='videos/')
    gif_file = models.ImageField(upload_to='gifs/', blank=True, null=True)
    image_file = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"Video {self.id}"