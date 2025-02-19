from account.serializer import UserSerializer
from rest_framework import serializers
import uuid
from .models import ChatMessage, Thread

class UplaodChatWithAttachmentSerializer(serializers.ModelSerializer):
    thread = serializers.SerializerMethodField()
    attached_file_name = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'sender', 
            'receiver',
            'message',
            'thread',
            'attached_file',
            'attached_file_name'          
        ]
    
    def create(self, validated_data):
        sender = self.context['request'].user
        validated_data['sender'] = sender
        receiver= validated_data['receiver']
        thread, created = Thread.threadm.get_or_new(sender, receiver.id)

        validated_data['thread'] = thread#setting the thread instance 

        attached_file = validated_data['attached_file']
        file_name = attached_file.name

        validated_data['attached_file_name'] = file_name

        attached_file.name = f"{str(uuid.uuid4())}.{file_name.split('.')[-1]}"

        return super().create(validated_data)

    


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    attached_file_size = serializers.SerializerMethodField()
    class Meta:
        model = ChatMessage
        fields = '__all__'

    def get_attached_file_size(self, obj):
        attached_file = getattr(obj, 'attached_file', None)

        if attached_file:
            file_size_bytes = attached_file.size
            file_size_mb = file_size_bytes / (1024*1024)
            if file_size_mb > 1:
                return "{:.2f}".format(file_size_mb) + 'MB'
            
            file_size_kb = file_size_bytes / 1024
            return "{:.2f}".format(file_size_kb) + 'KB'
        else:
            return '0kb'

class ThreadSerializer(serializers.ModelSerializer):
    user_one = UserSerializer()
    user_two = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = '__all__'
    
    def get_last_message(self, obj):
        last_message = ChatMessage.objects.filter(thread=obj).order_by('-created').first()
        return last_message.message