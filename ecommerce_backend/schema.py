# ecommerce_backend/schema.py

import graphene
from graphene_django import DjangoObjectType


# Types
class UserType(DjangoObjectType):
    pass


class CategoryType(DjangoObjectType):
    pass


class ProductType(DjangoObjectType):
    pass


class OrderItemType(DjangoObjectType):
    pass


class OrderType(DjangoObjectType):
    pass


# Queries
class Query(graphene.ObjectType):
    pass


# Mutations
class CreateUserMutation(graphene.Mutation):
    pass


class CreateProductMutation(graphene.Mutation):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
