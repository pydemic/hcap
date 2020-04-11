from ..env import env

# Used by users.validations.CPFValidator
VALIDATE_CPF = env("HCAP__VALIDATE_CPF", default=True)
