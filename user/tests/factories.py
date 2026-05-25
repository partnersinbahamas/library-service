import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "user-password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")

    is_staff = False
    is_superuser = False

    class Params:
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True,
        )
