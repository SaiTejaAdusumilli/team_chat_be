import graphene
from core.queries import Query, Subscription
from core.mutations import Mutation

schema = graphene.Schema(query=Query, mutation=Mutation,subscription=Subscription)