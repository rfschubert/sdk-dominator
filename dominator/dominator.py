import base64
import json

import requests, pendulum
from pycpfcnpj import cpf, cnpj, cpfcnpj
from .exceptions import InvalidCPFException, InvalidCNPJException, InvalidTaxIDException

SERPRO = {
    'api_url': 'https://apigateway.serpro.gov.br',
    'connection_retry_limit': 10,
    'consumer_key': 'tCMFnoBwH8sGia4_3T9v5_ZDGYka',
    'consumer_secret': 'xhzPD3Gbhz3HsYR9kMfIaLk_Lisa'
}


class Dominator:

    def validate_tax_id(self, tax_id, mock=None, user=None, cpf_django_model=None):
        if len(cpfcnpj.clear_punctuation(tax_id)) == 11:
            if not cpf.validate(tax_id):
                if user is not None:
                    try:
                        user.dominator_lock_account()
                    except:
                        pass

                raise InvalidCPFException
            else:
                try:
                    serpro = self.validate_tax_id_cpf_against_serpro(tax_id, mock, cpf_django_model)
                except:
                    raise

                if user is not None:
                    try:
                        user.dominator_is_valid_tax_id(serpro=serpro)
                    except:
                        pass

                return serpro

        if len(cpfcnpj.clear_punctuation(tax_id)) == 14:
            if not cnpj.validate(tax_id):
                raise InvalidCNPJException

            return True

        raise InvalidTaxIDException

    def validate_tax_id_cpf_against_serpro(self, cpf, mock=None, cpf_django_model=None):
        URL = SERPRO['api_url'] + "/consulta-cpf/v1/cpf/{}".format(cpfcnpj.clear_punctuation(cpf))

        headers = {
            'Authorization': 'Bearer ' + self.get_auth_token(),
            'Accept': 'application/json'
        }

        if mock is None:
            if cpf_django_model is not None:
                try:
                    cpf_model_object = cpf_django_model.objects.get(cpf=cpf)
                    if cpf_model_object.raw_data == {}:
                        cpf_model_object.delete()
                        cpf_model_object = None
                except:
                    cpf_model_object = None

            if cpf_django_model is None or cpf_model_object is None:
                response = requests.get(URL, headers=headers)
                if response.status_code == 400:
                    raise InvalidCPFException

                raw = json.loads(response.text)
            else:
                raw = cpf_model_object.raw_data
        else:
            if mock is False:
                raise InvalidCPFException
            raw = mock

        response = {
            "tax_id": "{}.{}.{}-{}".format(raw["ni"][:3], raw["ni"][3:6], raw["ni"][6:9], raw["ni"][9:11]),
            "name": raw["nome"],
            "birthday": pendulum.datetime(year=int(raw["nascimento"][4:8]), month=int(raw["nascimento"][2:4]), day=int(raw["nascimento"][:2])).date(),
            "raw": raw
        }

        if cpf_django_model is not None and cpf_model_object is None:
            try:
                cpf_django_model.objects.create(
                    cpf=response["tax_id"],
                    nome=response["name"],
                    situacao=response["raw"]["situacao"],
                    data_nascimento=response["birthday"],
                    raw_data=response["raw"],
                )
            except:
                print("error on store CPF on database")

        return response

    def get_auth_token(self):
        SECRET = base64.b64encode(str(SERPRO['consumer_key'] + ":" + SERPRO['consumer_secret']).encode()).decode()
        payload = "grant_type=client_credentials"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Basic " + SECRET
        }
        for i in range(10):
            try:
                response = requests.post(SERPRO['api_url'] + "/token", data=payload, headers=headers)
                response.raise_for_status()
            except Exception:
                return ''
            else:
                return response.json()['access_token']
        else:
            return False
