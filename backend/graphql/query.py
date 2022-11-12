import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from ..models import User as UserModel

from ..graphql.objects import UserObject as User


class Query(graphene.ObjectType):
   node = relay.Node.Field()

   users = graphene.List(lambda: User, email=graphene.String(), user_id=graphene.Int())


   def resolve_users(self, info, email=None):
       query = User.get_query(info)

       if email:
           query = query.filter(UserModel.email == email)
       return query.all()

   all_users = SQLAlchemyConnectionField(User.connection)