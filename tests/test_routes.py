
"""
Account API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase

from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once before test suite"""

    def setUp(self):
        """Runs before each test"""
        db.session.query(Account).delete()
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        """Runs once after each test case"""
        db.session.remove()

    ##################################################################
    # HELPER METHODS
    ##################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []

        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(
                BASE_URL,
                json=account.serialize(),
                content_type="application/json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )

            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)

        return accounts

    ##################################################################
    # ACCOUNT TEST CASES
    ##################################################################

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    def test_create_account(self):
        """It should create a new Account"""
        account = AccountFactory()

        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        location = response.headers.get("Location")
        self.assertIsNotNone(location)

        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["date_joined"], str(account.date_joined))

    def test_bad_request(self):
        """It should not create an Account with incomplete data"""
        response = self.client.post(
            BASE_URL,
            json={"name": "not enough data"},
            content_type="application/json",
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_unsupported_media_type(self):
        """It should reject an unsupported media type"""
        account = AccountFactory()

        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="test/html",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    def test_list_accounts(self):
        """It should list all accounts"""
        self._create_accounts(3)

        response = self.client.get(BASE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_read_account(self):
        """It should read an account by ID"""
        account = self._create_accounts(1)[0]

        response = self.client.get(f"{BASE_URL}/{account.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], account.id)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)

    def test_read_account_not_found(self):
        """It should return 404 when an account does not exist"""
        response = self.client.get(f"{BASE_URL}/999999")

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_update_account(self):
        """It should update an existing account"""
        account = self._create_accounts(1)[0]

        updated_data = {
            "name": "Updated Account",
            "email": "updated@example.com",
            "address": "Updated Address",
            "phone_number": "1234567890",
        }

        response = self.client.put(
            f"{BASE_URL}/{account.id}",
            json=updated_data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], account.id)
        self.assertEqual(data["name"], "Updated Account")
        self.assertEqual(data["email"], "updated@example.com")
        self.assertEqual(data["address"], "Updated Address")

    def test_update_account_not_found(self):
        """It should return 404 when updating a missing account"""
        updated_data = {
            "name": "Updated Account",
            "email": "updated@example.com",
            "address": "Updated Address",
            "phone_number": "1234567890",
        }

        response = self.client.put(
            f"{BASE_URL}/999999",
            json=updated_data,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_delete_account(self):
        """It should delete an account"""
        account = self._create_accounts(1)[0]

        response = self.client.delete(f"{BASE_URL}/{account.id}")

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_delete_account_not_found(self):
        """It should return 404 when deleting a missing account"""
        response = self.client.delete(f"{BASE_URL}/999999")

        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )
