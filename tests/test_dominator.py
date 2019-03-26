import pendulum

from dominator import Dominator

from unittest import TestCase

from dominator.exceptions import InvalidTaxIDException, InvalidCPFException, InvalidCNPJException
from tests.mocks import MockSERPRO, MockDjangoUserModel, MockDjangoCPFModel


class DominatorTestCase(TestCase):
    def setUp(self):
        self.FAKE_CPFs = [
            "12345678910", "123.456.789.10"
        ]

        self.FAKE_CNPJs = [
            "12345678000110", "12.345.678/0001-10"
        ]

        self.TRUE_CPFs = [
            "077.703.749-10", "07770374910"
        ]

        self.TRUE_CNPJs = [
            "15280995000169", "15.280.995/0001-69"
        ]

    def test_validate_tax_id(self):
        # validate user CPF
        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id(self.FAKE_CPFs[0])

        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id(self.FAKE_CPFs[0])

        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id(self.FAKE_CPFs[1])

        # validate user CNPJ
        with self.assertRaises(InvalidCNPJException):
            Dominator().validate_tax_id(self.FAKE_CNPJs[0])

        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id(self.FAKE_CNPJs[0])

        with self.assertRaises(InvalidCNPJException):
            Dominator().validate_tax_id(self.FAKE_CNPJs[1])

        Dominator().validate_tax_id(self.TRUE_CPFs[0], mock=MockSERPRO.get_cpf_0770374910())
        Dominator().validate_tax_id(self.TRUE_CPFs[1], mock=MockSERPRO.get_cpf_0770374910())
        Dominator().validate_tax_id(self.TRUE_CNPJs[0])
        Dominator().validate_tax_id(self.TRUE_CNPJs[1])

    def test_raise_error_if_invalid_tax_id(self):
        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id("123")

    def test_validate_tax_id_cpf_against_serpro(self):
        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id_cpf_against_serpro(self.FAKE_CPFs[0], mock=MockSERPRO.get_invalid())

        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id_cpf_against_serpro(self.FAKE_CPFs[1], mock=MockSERPRO.get_invalid())

        self.assertEqual(
            Dominator().validate_tax_id_cpf_against_serpro(self.TRUE_CPFs[0], mock=MockSERPRO.get_cpf_0770374910()),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.date(year=1992, month=2, day=10),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )

        self.assertEqual(
            Dominator().validate_tax_id_cpf_against_serpro(self.TRUE_CPFs[1], mock=MockSERPRO.get_cpf_0770374910()),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.datetime(year=1992, month=2, day=10).date(),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )

        self.assertEqual(
            Dominator().validate_tax_id(self.TRUE_CPFs[0]),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.date(year=1992, month=2, day=10),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )

    def test_lock_user_account_if_invalid_tax_id(self):
        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id(
                self.FAKE_CPFs[0],
                mock=MockSERPRO.get_invalid(),
                user=MockDjangoUserModel()
            )

    def test_get_from_database_django(self):
        # cpf exists, raw data is None
        self.assertEqual(
            Dominator().validate_tax_id("077.703.749-10", cpf_django_model=MockDjangoCPFModel().get("raw_data")),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.date(year=1992, month=2, day=10),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )
        # cpf exists, raw data is Valid
        self.assertEqual(
            Dominator().validate_tax_id("077.703.749-10", cpf_django_model=MockDjangoCPFModel().get("077.703.749-10")),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.date(year=1992, month=2, day=10),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )
        # cpf do not exists
        self.assertEqual(
            Dominator().validate_tax_id("077.703.749-10", cpf_django_model=MockDjangoCPFModel().get(None)),
            {
                "tax_id": "077.703.749-10",
                "name": "RAPHAEL FILIPE SCHUBERT",
                "birthday": pendulum.date(year=1992, month=2, day=10),
                "raw": {
                    "ni": "07770374910",
                    "nome": "RAPHAEL FILIPE SCHUBERT",
                    "nascimento": "10021992",
                    "situacao": {
                        "codigo": "0", "descricao": "Regular"
                    }
                }
            }
        )

    def test_calculate_user_coefficient(self):
        pass
