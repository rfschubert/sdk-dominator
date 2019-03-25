from dominator import Dominator

from unittest import TestCase

from dominator.exceptions import InvalidTaxIDException, InvalidCPFException, InvalidCNPJException


class DominatorTestCase(TestCase):
    def setUp(self):
        self.FAKE_CPFS = [
            "12345678910", "123.456.789.10"
        ]

        self.FAKE_CNPJS = [
            "12345678000110", "12.345.678/0001-10"
        ]

    def test_validate_tax_id(self):
        # validate user CPF
        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id(self.FAKE_CPFS[0])

        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id(self.FAKE_CPFS[0])

        with self.assertRaises(InvalidCPFException):
            Dominator().validate_tax_id(self.FAKE_CPFS[1])

        # validate user CNPJ
        with self.assertRaises(InvalidCNPJException):
            Dominator().validate_tax_id(self.FAKE_CNPJS[0])

        with self.assertRaises(InvalidTaxIDException):
            Dominator().validate_tax_id(self.FAKE_CNPJS[0])

        with self.assertRaises(InvalidCNPJException):
            Dominator().validate_tax_id(self.FAKE_CNPJS[1])

# todo: validate against SERPRO
# todo: lock user account
