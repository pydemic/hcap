from hcap.settings.env import env

# Used by hcap_accounts.validations.CPFValidator
VALIDATE_CPF = env("HCAP__VALIDATE_CPF", default=True)
