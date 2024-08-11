from faker import Faker

fake = Faker()


class User:
    @staticmethod
    def register_new_user():
        return {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.user_name()
        }

    @staticmethod
    def register_new_user_without_name():
        return {
            "email": fake.email(),
            "password": fake.password(),
        }

    @staticmethod
    def update_user_data():
        return {
            "email": fake.email(),
            "name": fake.user_name()
        }
