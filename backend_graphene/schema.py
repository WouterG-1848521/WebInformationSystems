import graphene

from .graphql.query import Query

schema = graphene.Schema(query=Query)