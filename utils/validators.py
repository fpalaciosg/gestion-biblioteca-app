"""
Validadores - Funciones de validación de datos
"""
import re


def validar_rut(rut: str) -> bool:
    """Valida que el RUT tenga formato válido (sin validar dígito verificador)"""
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "")
    return len(rut_limpio) >= 7 and rut_limpio.isalnum()


def validar_isbn(isbn: str) -> bool:
    """Valida que el ISBN sea válido (básico)"""
    isbn_limpio = isbn.replace("-", "").replace(" ", "")
    # Puede ser ISBN-10 o ISBN-13
    return len(isbn_limpio) in [10, 13] and isbn_limpio.isdigit()


def validar_titulo(titulo: str) -> bool:
    """Valida que el título no esté vacío"""
    return bool(titulo.strip()) and len(titulo) <= 200


def validar_autor(autor: str) -> bool:
    """Valida que el autor no esté vacío"""
    return bool(autor.strip()) and len(autor) <= 150


def validar_nombre(nombre: str) -> bool:
    """Valida que el nombre no esté vacío"""
    return bool(nombre.strip()) and len(nombre) <= 150


def limpiar_rut(rut: str) -> str:
    """Limpia el RUT removiendo puntos y guiones"""
    return rut.replace(".", "").replace("-", "").replace(" ", "")


def formatear_rut(rut: str) -> str:
    """Formatea un RUT limpio al formato XX.XXX.XXX-X"""
    rut_limpio = limpiar_rut(rut)
    if len(rut_limpio) < 8:
        return rut
    
    # Extraer partes
    cuerpo = rut_limpio[:-1]
    verificador = rut_limpio[-1]
    
    # Formatear
    return f"{cuerpo[-6:]}.{cuerpo[-9:-6]}.{cuerpo[:-6]}-{verificador}".lstrip("0").lstrip(".")
