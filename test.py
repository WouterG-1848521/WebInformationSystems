## define schema

import graphene
import datetime

class ProfileTypes(graphene.Enum):
    ADMIN = 1
    USER = 2

class UserInfo(graphene.ObjectType):
    graduation_date = graphene.Date(required=True)
    experience = graphene.String()

    def resolve_graduation_date(self, info):
        return self.graduation_date

class User(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    profile_type = graphene.Field(ProfileTypes)
    information = graphene.Field(UserInfo)
    connections = graphene.List(graphene.NonNull(lambda: Connection))

    def resolve_information(self, info):
        return get_user_info(self.information)

    def resolve_connections(self, info):
        return [get_connection(s) for s in self.connections]


class VacancyInfo(graphene.ObjectType):
    description = graphene.String(required=True)
    requirements = graphene.String(required=True)

class Vacancy(graphene.ObjectType):
    id = graphene.ID(required=True)
    job_title = graphene.String(required=True)
    start_date = graphene.Date(required=True)
    end_date = graphene.Date(required=True)
    address = graphene.String(required=True)
    available = graphene.Boolean(required=True)
    owned_by = graphene.Field(lambda: Enterprise, required=True)
    information = graphene.String(required=True)


    def resolve_vacancy_info(self, info):
        return self.vacancy_info

    def resolve_connections(self, info):
        return self.connections

    def resolve_owned_by(self, info):
        return self.owned_by

class Connection(graphene.ObjectType):
    id = graphene.ID(required=True)
    from_user = graphene.NonNull(User)
    to_user = graphene.NonNull(User)
    acknowledged = graphene.Boolean(required=True)

    def resolve_from_user(self, info):
        print("resolve_from_user")
        return get_user(self.from_user)

    def resolve_to_user(self, info):
        return get_user(self.to_user)

class EnterpriseInfo(graphene.ObjectType):
    info = graphene.String()

  
class Enterprise(graphene.ObjectType):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    address = graphene.List(graphene.NonNull(graphene.String), required=True)
    maintainers = graphene.List(User, required=True)
    information = graphene.NonNull(EnterpriseInfo)

    def resolve_maintainers(self, info):
        return self.maintainers


class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.ID(required=True))

    def resolve_user(root, info, id):
        print("resolve_user")
        return get_user(id)

    def resolve_users(root, info):
        print("resolve_users")
        return get_all_users()

schema = graphene.Schema(query=Query)

users_data = {}
user_info_data = {}
connection_data = {}

def setup():
    
    global users_data, user_info_data, connection_data

    brent = User(
        id='1',
        name='Brent',
        email = '@email.com',
        password = '123',
        profile_type = ProfileTypes.USER,
        information = "1",
        connections = ['1']
    )

    users_data = {
        "1": brent
    }

    user_info_data = {
        "1": UserInfo(graduation_date=datetime.date(2019, 1, 1), experience="10 years")
    }

    connection_data = {
        "1": Connection(id="1", 
        from_user="1", to_user="1", 
        acknowledged=True)
    }
    

def get_all_users():
    print("getting all user data")
    return list(users_data.values())

def get_user(id):
    print("getting user data")
    return users_data.get(id)

def get_user_info(id):
    return user_info_data.get(id)

def get_connection(id):
    return connection_data.get(id)

setup()


query = """
    query users {
      users {
        name,
        email,
        password,
        profileType,
        information {
            graduationDate,
            experience
        },
        connections {
            acknowledged,
            fromUser {
                name
            },
            toUser {
                name
            }
        }
      }
    }
"""
result = schema.execute(query)
print(query)
print(result)
print(result.data["users"])

