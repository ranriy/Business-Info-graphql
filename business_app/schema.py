import graphene
from graphene_django import DjangoObjectType
from graphene import Argument

from business_app.models import Company
from django.contrib.auth.models import User

class CompanyType(DjangoObjectType):
    class Meta:
        model = Company

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_companies = graphene.List(CompanyType)
    company_by_name = graphene.Field(CompanyType, name=graphene.String(required=True))

    all_owners = graphene.List(UserType)
    user_by_name = graphene.Field(UserType, name=graphene.String(required=True))

    def resolve_all_companies(root, info):
        return Company.objects.all()

    def resolve_company_by_name(root, info, name):
        try:
            return Company.objects.get(name=name)
        except Company.DoesNotExist:
            return None

    def resolve_all_owners(root, info):
        return User.objects.all()

    def resolve_owner_by_name(root, info, name):
        try:
            return User.objects.get(name=name)
        except User.DoesNotExist:
            return None

class CreateCompany(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        address = graphene.String()
        owners = graphene.List(graphene.ID) 
        employee_size = graphene.Int()
        created_at = graphene.types.datetime.DateTime()
        updated_at = graphene.types.datetime.DateTime()


    company = graphene.Field(CompanyType)

    def mutate(self, info, name, address=None, owners=None, employee_size=True, created_at=None, updated_at=None):
        company = Company.objects.create(
            name = name,
            address = address,
            employee_size = employee_size,
            created_at = created_at,
            updated_at = updated_at
        )

        if owners is not None:
            owner_set = []
            for owner_id in owners:
                owner_object = User.objects.get(pk=owner_id)
                owner_set.append(owner_object)
            company.owners.set(owner_set)

        company.save()
        return CreateCompany(company=company)

class UpdateCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        address = graphene.String()
        owners = graphene.List(graphene.ID) 
        employee_size = graphene.Int()
        created_at = graphene.types.datetime.DateTime()
        updated_at = graphene.types.datetime.DateTime()

    company = graphene.Field(CompanyType)

    def mutate(self, info, id, name=None, address=None, owners=None, employee_size=True, created_at=None, updated_at=None):
        company = Company.objects.get(pk=id)
        company.name = name if name is not None else company.name
        company.address = address if address is not None else company.address
        company.employee_size = employee_size if employee_size is not None else company.employee_size
        company.created_at = created_at if created_at is not None else company.created_at
        company.updated_at = updated_at if updated_at is not None else company.updated_at

        if owners is not None:
            owner_set = []
            for owner_id in owners:
                owner_object = User.objects.get(pk=owner_id)
                owner_set.append(owner_object)
            company.owners.set(owner_set)

        company.save()
        return UpdateCompany(company=company)


class DeleteCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    company = graphene.Field(CompanyType)

    def mutate(self, info, id):
        company = Company.objects.get(pk=id)
        if company is not None:
            company.delete()
        return DeleteCompany(company=company)

class CreateOwner(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        username = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, first_name, username, last_name=None, email=None):
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username
        )
        user.save()
        return CreateOwner(user=user)

class UpdateOwner(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        email = graphene.String()

     
    user = graphene.Field(UserType)

    def mutate(self, info, id, first_name, email=None):
        user = User.objects.get(pk=id)
        user.first_name = first_name if first_name is not None else user.first_name
        user.email = email if email is not None else user.email
        user.save()
        return UpdateOwner(user=user)


class DeleteOwner(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    user = graphene.Field(UserType)

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        if user is not None:
            user.delete()
        return DeleteOwner(user=user)

class Mutation(graphene.ObjectType):
    create_company = CreateCompany.Field()
    update_company = UpdateCompany.Field()
    delete_company = DeleteCompany.Field()

    create_owner = CreateOwner.Field()
    update_owner = UpdateOwner.Field()
    delete_owner = DeleteOwner.Field()
            
schema = graphene.Schema(query=Query, mutation=Mutation)