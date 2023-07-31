from django.db import models

# Create your models here.

class Board(models.Model):
    bNum = models.AutoField(primary_key=True,auto_created=1000)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=3000,null=True,blank=True)
    author = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL,null=True
        ,related_name="boards"
        )
    file = models.FileField(blank=True,null=True)
    image_url  = models.URLField(default = '')
    createdAt = models.DateTimeField("작성일", auto_now_add=True)
    modifiedAt = models.DateTimeField("수정일", auto_now=True)
    

