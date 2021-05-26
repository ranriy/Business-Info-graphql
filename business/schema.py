import graphene
import business_app.schema

class Query(business_app.schema.Query, graphene.ObjectType):
    pass
class Mutation(business_app.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)