def validador_contraseñas(passw):
    if len(passw) > 8:
        is_upper = 0
        is_digit = 0
        is_char_special = 0
        is_lower = 0
        for char in passw:
            if char.islower(): is_lower += 1
            elif char.isupper(): is_upper += 1
            elif char.isdigit(): is_digit += 1
            elif char in '#$%&/()¡!¿?[]{}<>"': is_char_special += 1   
        if is_upper == 0: return "Le hace falta minimo una mayuscula"
        elif is_digit == 0: return "Le hace falta minimo un número"
        elif is_char_special == 0: return "Le hace falta minimo un caracter especial"
        elif is_lower == 0: return "Le hace falta minimo una minuscula"
        print("Contraseña segura")
        return True
    return "Contraseña muy corta, debe ser mayor a 8 caracteres"


def validador_usuarios(user, dicc):
    if len(user) <= 6:
        return "Nombre de usuario muy corto"
    else:
        if user in dicc:
            return "Usuario ya existente, elige otro usuario"
        else:
            print("Usuario disponible :)")
            return True