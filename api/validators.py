from django.core.validators import RegexValidator

# Regexs
user_names = {"regex": "^([a-zA-ZñÑáéíóúÁÉÍÓÚ ]{1,30})$", "msg": "Utilice solo letras"}
cell_phone_number = {
    "regex": "^([0-9]{10})$",
    "msg": "Utilice solo números (no se acepta espacios)",
}
dni = {"regex": "^([0-9]{4,20})$", "msg": "Utilice solo números, longitud 4-20"}

city_name = {"regex": "^([a-zA-ZñÑáéíóúÁÉÍÓÚ ]{1,40})$", "msg": "Utilice solo letras"}
address = {
    "regex": "^([a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ#._ -]{1,40})$",
    "msg": "Utilice solo letras y números (solo se aceptan los símbolos #._-)",
}

desk_number = {"regex": "^([0-9]{1,4})$", "msg": "Utilice solo números, longitud 1-4"}

book_isbn = {"regex": "^([0-9]{13})$", "msg": "Utilice solo números, la longitud debe ser de 13 dígitos"}


# Models´s RegexValidators
ESTUDIANTE_REGEXS = {
    "dni": RegexValidator(regex=dni["regex"], message=dni["msg"], code="Invalid DNI"),
    "nombres": RegexValidator(
        regex=user_names["regex"], message=user_names["msg"], code="Invalid name"
    ),
    "apellidos": RegexValidator(
        regex=user_names["regex"], message=user_names["msg"], code="Invalid lastname"
    ),
    "celular": RegexValidator(
        regex=cell_phone_number["regex"],
        message=cell_phone_number["msg"],
        code="Invalid cell phone number",
    ),
}


LIBRO_REGEXS = {
    "isbn": RegexValidator(
        regex=book_isbn["regex"], message=book_isbn["msg"], code="Invalid ISBN"
    ),
}
