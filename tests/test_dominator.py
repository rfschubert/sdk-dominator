from dominator import Dominator

from unittest import TestCase

from dominator.exceptions import InvalidTaxIDException, InvalidCPFException, InvalidCNPJException


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

        Dominator().validate_tax_id(self.TRUE_CPFs[0])
        Dominator().validate_tax_id(self.TRUE_CPFs[1])
        Dominator().validate_tax_id(self.TRUE_CNPJs[0])
        Dominator().validate_tax_id(self.TRUE_CNPJs[1])

# todo: validate against SERPRO
# todo: lock user account
