from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Messages(models.Model):
    content = models.CharField(max_length=200)
    sent_by = models.ForeignKey(User, related_name="messages_sent", on_delete=models.DO_NOTHING)
    sent_to = models.ForeignKey(User, related_name="messages_received", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    member = models.ManyToManyField(User, related_name="rooms")

    def __str__(self) -> str:
        return str(self.id)

    

    def get_online_count(self):
        return self.member.count()


    def join(self, user):
        self.member.add(user)
        self.save()

    def leave(self, user):
        self.member.remove(user)
        self.save()





