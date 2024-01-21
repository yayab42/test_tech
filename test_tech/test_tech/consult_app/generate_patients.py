import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_tech.test_tech.settings')
django.setup()

import logging
import requests
from faker import Faker
from django.contrib.auth.models import User
from django.db import transaction
from consult_app.models import Patient, Address
from consult_app.models import AppUser, Address, Patient, Doctor

fake = Faker()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_fake_address():
    response = requests.get('https://apicarto.ign.fr/api/codes-postaux/communes/26400',
                            headers={'accept': 'application/json'})
    data = response.json()

    address_data = fake.random_element(data)

    return {
        'postal_code': address_data['codePostal'],
        'city': address_data['nomCommune'],
        'address': address_data['libelleAcheminement'],
    }


@transaction.atomic
def create_fake_patients(num_patients):
    i = 1
    for _ in range(num_patients):
        fake_address = generate_fake_address()

        first_name = fake.first_name()
        base_username = first_name
        username = base_username
        count = 1

        while User.objects.filter(username=username).exists():
            count += 1
            username = f"{base_username}{count}"

        user = User.objects.create(
            username=username,
            password='password',
        )

        app_user = AppUser.objects.create(
            user=user,
            user_type='patient',
        )

        address = Address.objects.create(
            postal_code=fake_address['postal_code'],
            city=fake_address['city'],
            address=fake_address['address'],
        )

        patient = Patient.objects.create(
            app_user=app_user,
            name=fake.last_name(),
            surname=user.username,
            email=fake.email(),
            address=address,
        )

        logger.info(f"Patient {i} : {username} créé")
        i = i + 1


def create_doctor():
    user = User.objects.create(
        username='Yannis',
        password='password',
    )

    app_user = AppUser.objects.create(
        user=user,
        user_type='doctor',
    )

    doctor = Doctor.objects.create(
        app_user=app_user,
        name='Yannis',
        surname='Doctor',
    )

    logger.info("Docteur Yannis créé")


if __name__ == "__main__":
    # create_fake_patients(5000)
    create_doctor()
    print("Done")
