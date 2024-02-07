from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random

class User(AbstractUser):
    unqname = models.CharField(max_length=30, unique=True, blank=True)

    def save(self, *args, **kwargs):
        random_number = random.randint(1000, 9999)
        fn = self.first_name.replace(" ", "")
        ln = self.last_name.replace(" ", "")
        self.unqname = f"{fn.lower()[:4]}{ln.lower()[:4]}#{random_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.unqname

# user = User.objects.create(username='example', email='example@example.com')
# user.set_password('securepassword')
# user.save()


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sessions')
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='other_user_sessions')
    # timestamp = models.DateTimeField(default=timezone.now())


    class Meta:
        unique_together = ['user', 'other_user']

    def __str__(self):
        return f"{self.user} with {self.other_user}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete = models.CASCADE, related_name = 'chat_window')

    # def save(self, *args, **kwargs):
    #     # Update the associated Session's timestamp with the message's timestamp
    #     self.session.timestamp = timezone.now()
    #     self.session.save()
    #     print("session: ",self.session)
    #     print("times",self.session.timestamp,self.timestamp)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"



class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} in {self.group}"

class GroupMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.group}"



