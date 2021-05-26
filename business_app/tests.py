import json
import pytest
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth.models import User
from graphene_django.utils.testing import graphql_query
from .models import Company


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func

@pytest.mark.django_db
def test_allowners_query(client_query):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
 
    response = client_query(
        '''
        query {
            allOwners {
                firstName
                lastName
            }
        }
        '''
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert len(content["data"]["allOwners"]) == 1

@pytest.mark.django_db
def test_allcompanies_query(client_query):
    response = client_query(
        '''
        query {
            allCompanies {
                name
                address
                owners {
                    firstName
                    lastName
                }
                employeeSize
    
            }
        }
        '''
    )
    content = json.loads(response.content)
    assert 'errors' not in content


        