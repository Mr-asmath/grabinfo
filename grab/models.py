from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    image = models.ImageField(default='image/userprofile.png', upload_to=getFileName)
    bio = models.TextField(max_length=100, blank=True)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Topic(models.Model):
    topic_name=models.CharField(max_length=100,blank=False,null=False)
    def __str__(self):
        return self.topic_name
    
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField()
    post_image=models.ImageField(blank=False,null=False)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f'Post by {self.profile.user.username} on {self.topic.topic_name}'


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow_relationship')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.user.username} follows {self.following.user.username}'


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'post'], name='unique_post_like')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.profile.user.username} likes post {self.post_id}'


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.profile.user.username} on post {self.post_id}'


class Save(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'post'], name='unique_saved_post')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.profile.user.username} saved post {self.post_id}'
