import graphene

from backend_graphene import db
from ..graphql.objects import User
from ..models import User as UserModel


class UserMutation(graphene.Mutation):
   class Arguments:
       email = graphene.String(required=True)

   user = graphene.Field(lambda: User)

   def mutate(self, info, email):
       user = UserModel(email=email)

       db.session.add(user)
       db.session.commit()

       return UserMutation(user=user)

class Mutations(graphene.ObjectType):
    add_user = UserMutation.Field()