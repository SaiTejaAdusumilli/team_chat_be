# schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Message, User, Session

class MessageType(DjangoObjectType):
    class Meta:
        model = Message

class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        sender = graphene.String(required=True)
        receiver = graphene.String(required=True)
        content = graphene.String(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, **kwargs):
        sender = kwargs['sender']
        receiver = kwargs['receiver']
        content = kwargs['content']
        sender = User.objects.get(unqname=sender)
        receiver = User.objects.get(unqname=receiver)
        session, created =  Session.objects.get_or_create(user=sender,other_user = receiver)
        message = Message(sender=sender, receiver=receiver, content=content, session = session)
        message.save()
        print("created message")

        return CreateMessageMutation(message=message)

class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
