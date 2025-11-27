"""
Módulo de validación de licencias.
Verifica si la aplicación está activada y si la licencia es válida.
"""

import os
from datetime import datetime
from .hwid import get_hwid
from .crypto import LicenseCrypto


class LicenseValidator:
    """Clase para validar licencias de la aplicación."""

    # Ruta del archivo de licencia (en %APPDATA%)
    LICENSE_DIR = os.path.join(os.getenv('APPDATA'), 'GestionComercial')
    LICENSE_FILE = os.path.join(LICENSE_DIR, 'license.dat')

    @staticmethod
    def ensure_license_dir():
        """Asegura que el directorio de licencias existe."""
        if not os.path.exists(LicenseValidator.LICENSE_DIR):
            os.makedirs(LicenseValidator.LICENSE_DIR)

    @staticmethod
    def is_activated():
        """
        Verifica si la aplicación está activada.

        Returns:
            bool: True si está activada, False en caso contrario
        """
        if not os.path.exists(LicenseValidator.LICENSE_FILE):
            return False

        license_data = LicenseCrypto.read_license_file(LicenseValidator.LICENSE_FILE)
        if not license_data:
            return False

        # Verifica que el HWID coincida
        current_hwid = get_hwid()
        stored_hwid = license_data.get('hwid', '')

        if current_hwid != stored_hwid:
            return False

        return True

    @staticmethod
    def activate(license_code):
        """
        Activa la aplicación con un código de licencia.

        Args:
            license_code (str): Código de licencia proporcionado por el usuario

        Returns:
            tuple: (success: bool, message: str)
        """
        current_hwid = get_hwid()

        # Valida el formato del código
        if not license_code or len(license_code.replace('-', '')) < 10:
            return False, "Código de licencia inválido"

        # Valida el código contra el HWID
        validation_result = LicenseCrypto.validate_license_code(license_code, current_hwid)

        if not validation_result:
            return False, "El código de licencia no es válido"

        # Crea el archivo de licencia
        try:
            LicenseValidator.ensure_license_dir()
            LicenseCrypto.create_license_file(
                current_hwid,
                license_code,
                LicenseValidator.LICENSE_FILE
            )
            return True, "Licencia activada correctamente"

        except Exception as e:
            return False, f"Error al guardar la licencia: {e}"

    @staticmethod
    def get_license_info():
        """
        Obtiene información de la licencia actual.

        Returns:
            dict: Información de la licencia o None si no está activada
        """
        if not os.path.exists(LicenseValidator.LICENSE_FILE):
            return None

        license_data = LicenseCrypto.read_license_file(LicenseValidator.LICENSE_FILE)
        return license_data

    @staticmethod
    def deactivate():
        """
        Desactiva la aplicación eliminando el archivo de licencia.
        Útil para testing o soporte.
        """
        if os.path.exists(LicenseValidator.LICENSE_FILE):
            os.remove(LicenseValidator.LICENSE_FILE)

    @staticmethod
    def validate_on_startup():
        """
        Validación completa al iniciar la aplicación.

        Returns:
            tuple: (is_valid: bool, message: str, requires_activation: bool)
        """
        # Verifica si existe el archivo de licencia
        if not os.path.exists(LicenseValidator.LICENSE_FILE):
            return False, "La aplicación no está activada", True

        # Lee el archivo de licencia
        license_data = LicenseCrypto.read_license_file(LicenseValidator.LICENSE_FILE)
        if not license_data:
            return False, "Archivo de licencia corrupto", True

        # Verifica el HWID
        current_hwid = get_hwid()
        stored_hwid = license_data.get('hwid', '')

        if current_hwid != stored_hwid:
            return False, "Esta licencia está vinculada a otro equipo", True

        # Todo OK
        return True, "Licencia válida", False


if __name__ == "__main__":
    # Prueba del módulo
    print("=== Test del módulo de validación ===")

    print(f"\n¿Está activada? {LicenseValidator.is_activated()}")

    # Obtener información
    info = LicenseValidator.get_license_info()
    if info:
        print(f"Información de licencia: {info}")
    else:
        print("No hay información de licencia")

    # Test de validación en startup
    is_valid, message, needs_activation = LicenseValidator.validate_on_startup()
    print(f"\nValidación en startup:")
    print(f"  Válida: {is_valid}")
    print(f"  Mensaje: {message}")
    print(f"  Requiere activación: {needs_activation}")
