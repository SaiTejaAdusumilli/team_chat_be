import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from core.models import Message,User,Session,Group,UserGroup,GroupMessage

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("first_name","last_name","unqname","email")

class SessionType(DjangoObjectType):
    class Meta:
        model = Session
        fields = "__all__"

class CustomSessionType(graphene.ObjectType):
    session = graphene.Field(SessionType)
    message = graphene.String()

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = "__all__"

class UserGroupType(DjangoObjectType):
    class Meta:
        model = UserGroup
        fields = "__all__"

class GroupMessageType(DjangoObjectType):
    class Meta:
        model = GroupMessage
        fields = "__all__"

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    chats_of_user = graphene.List(CustomSessionType, user_email=graphene.String(required=True))
    get_user_chats = graphene.List(MessageType,sender=graphene.String(required = True), receiver = graphene.String(required=True))
    user_profile = graphene.Field(UserType,user_email=graphene.String(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_chats_of_user(root, info, user_email):
        try:
            user = User.objects.get(email = user_email)
            sessions =  Session.objects.filter(user=user)
            chat_window = []
            for session in sessions:
                message =  Message.objects.filter(Q(sender=session.user, receiver=session.other_user) | Q(sender=session.other_user, receiver=session.user)).last().content
                chat_window.append(CustomSessionType(session=session, message=message))
            return chat_window
        except:
            return None
    
    def resolve_get_user_chats(root, info, sender, receiver):
        return Message.objects.filter(Q(sender=User.objects.get(unqname=sender), receiver=User.objects.get(unqname=receiver)) | Q(sender=User.objects.get(unqname=receiver), receiver=User.objects.get(unqname=sender))).order_by("timestamp") 

    def resolve_user_profile(root,info,user_email):
        return User.objects.get(email = user_email)

class Subscription(graphene.ObjectType):

    message_updated = graphene.Field(MessageType, sender=graphene.String(), receiver=graphene.String())

    async def resolve_message_updated(root, info, sender, receiver):
        messages =  Message.objects.filter(Q(sender=User.objects.get(unqname=sender), receiver=User.objects.get(unqname=receiver)) | Q(sender=User.objects.get(unqname=receiver), receiver=User.objects.get(unqname=sender))) 
        print(messages.last(),"messages")
        return messages.last()