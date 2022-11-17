import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import User as UserModel


class UserObject(SQLAlchemyObjectType):
   user_id = graphene.Int(source='id')
   email = graphene.String(source='email')

   class Meta:
       model = UserModel
    #    interfaces = (relay.Node, )