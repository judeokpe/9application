from django.db import models
from account.models import CustomUser
from django.db.models import Q

# Create your models here.


class ThreadManager(models.Manager):
    def by_user(self, user):
        """
        Get the thread related to User user
        """
        lookup_one = Q(user_one=user) | Q(user_two=user)
        lookup_two = Q(user_one=user) & Q(user_two=user)#A user cannot have a thread with himself

        qs = self.get_queryset().filter(lookup_one).exclude(lookup_two)
        return qs
    
    def get_thread(self, user_one_id, user_two_id):
        if user_one_id == user_two_id:
            return None
        
        qLookup_one = Q(user_one__id=user_one_id) & Q(user_two__id = user_two_id)
        qLookup_two = Q(user_one__id=user_two_id) & Q(user_two__id=user_one_id)

        query_set = self.get_queryset().filter(qLookup_one | qLookup_two)
        return query_set
    
    def get_or_new(self, user, other_userId):
        """
        gets or creates a new thread related to User user and user with an id of other_userId
        returns Thread (created or found thread object), Boolean(true if a new thread was created, false otherwise)
        """

        userId = user.id
        if userId == other_userId:
            return None, False
        
        qlookup_one = Q(user_one__id=userId) & Q(user_two__id=other_userId)
        qlookup_two = Q(user_one__id=other_userId) & Q(user_two__id=userId)

        query_set = self.get_queryset().filter(qlookup_one | qlookup_two).distinct()

        if query_set.count() == 1:
            return query_set.first(), False
        elif query_set.count() > 1:
            return query_set.order_by('created').first(), False
        else:
            try:
                other_user = CustomUser.objects.get(id=other_userId)
            except CustomUser.DoesNotExist:
                return None, False

            if user != other_user:
                obj = self.model(
                    user_one = user,
                    user_two = other_user
                )

                obj.save()
                return obj, True
            
            return None, False



class Thread(models.Model):
    user_one = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='thread_user_one')
    user_two = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='thread_user_two')
    craeted = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    threadm = ThreadManager()

    def __str__(self) -> str:
        return f'{self.user_one.email} <-> {self.user_two.email}'
    

class ChatManager(models.Manager):
    def craete_chat(self, sender, receiverId, message, thread, commit=True):
        
        if sender.id == receiverId:
            return None, 'Sender and receiver cannot be thesame'
        
        receiver = CustomUser.objects.filter(id=receiverId).first()
        if receiver is not None:
            obj = self.model(
                thread=thread,
                sender=sender,
                receiver = receiver,
                message=message
            )

            if commit:
                obj.save()
            return obj, 'Chat created'
        else:
            return None, 'Receiver was not found'



class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=False, blank=False, related_name='msgthread')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='msgs_sent')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='msgs_received')
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    attached_file = models.FileField(upload_to='attachments/%Y/%M/%d', default=None, blank=True, null=True)
    attached_file_name = models.CharField(max_length=255, default=None, null=True, blank=True)

    objects = models.Manager()
    chatm= ChatManager()

    @property
    def get_attached_file_url(self):
        if self.attached_file:
            return self.attached_file.url
        return None
    
    @property
    def get_attached_file_size(self): 
        attached_file = self.attached_file
        if attached_file:
            file_size_bytes = attached_file.size
            file_size_mb = file_size_bytes / (1024*1024)
            if file_size_mb > 1:
                return "{:.2f}".format(file_size_mb) + 'MB'
            
            file_size_kb = file_size_bytes / 1024
            return "{:.2f}".format(file_size_kb) + 'KB'
        else:
            return '0kb'

    class Meta: 
        ordering = ['-created']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['-created'])
        ]
    
    