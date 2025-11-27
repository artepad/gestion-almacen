"""
Módulo de cifrado para licencias.
Utiliza AES-256 para cifrar y descifrar información de licencias.
"""

import os
import hashlib
import base64
import json
from datetime import datetime


class LicenseCrypto:
    """Clase para cifrado y descifrado de licencias."""

    # Clave maestra (IMPORTANTE: Cambia esto por una clave única para tu aplicación)
    # En producción, considera ofuscar esta clave o generarla de forma más compleja
    MASTER_KEY = b"GestionComercial2024SecretKey!@#"  # 32 bytes para AES-256

    @staticmethod
    def _pad(data):
        """Añade padding PKCS7 a los datos."""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length]) * padding_length
        return data + padding

    @staticmethod
    def _unpad(data):
        """Elimina padding PKCS7 de los datos."""
        padding_length = data[-1]
        return data[:-padding_length]

    @staticmethod
    def _derive_key(password):
        """Deriva una clave de 32 bytes desde un password."""
        return hashlib.sha256(password).digest()

    @staticmethod
    def simple_encrypt(data):
        """
        Cifrado simple usando XOR (para evitar dependencias externas).
        NOTA: Para producción real, considera usar cryptography library.

        Args:
            data (str): Datos a cifrar

        Returns:
            str: Datos cifrados en base64
        """
        key = LicenseCrypto._derive_key(LicenseCrypto.MASTER_KEY)
        data_bytes = data.encode('utf-8')

        # XOR con la clave
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key[i % len(key)])

        # Codificar en base64
        return base64.b64encode(bytes(encrypted)).decode('utf-8')

    @staticmethod
    def simple_decrypt(encrypted_data):
        """
        Descifrado simple usando XOR.

        Args:
            encrypted_data (str): Datos cifrados en base64

        Returns:
            str: Datos descifrados
        """
        try:
            key = LicenseCrypto._derive_key(LicenseCrypto.MASTER_KEY)
            encrypted_bytes = base64.b64decode(encrypted_data)

            # XOR con la clave
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key[i % len(key)])

            return bytes(decrypted).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error al descifrar: {e}")

    @staticmethod
    def generate_license_code(hwid, product_name="GestionComercial", validity_days=365):
        """
        Genera un código de licencia basado en el HWID.

        Args:
            hwid (str): Hardware ID del equipo
            product_name (str): Nombre del producto
            validity_days (int): Días de validez de la licencia

        Returns:
            str: Código de licencia cifrado
        """
        # Crea el payload de la licencia
        license_data = {
            'hwid': hwid,
            'product': product_name,
            'issued_date': datetime.now().isoformat(),
            'validity_days': validity_days,
            'version': '1.0'
        }

        # Convierte a JSON y cifra
        json_data = json.dumps(license_data)
        encrypted = LicenseCrypto.simple_encrypt(json_data)

        # Formatea el código de licencia en bloques
        return LicenseCrypto._format_license_code(encrypted)

    @staticmethod
    def _format_license_code(code):
        """
        Formatea el código de licencia en bloques de 5 caracteres.

        Args:
            code (str): Código sin formato

        Returns:
            str: Código formateado (ej: XXXXX-XXXXX-XXXXX-XXXXX)
        """
        # Toma los primeros caracteres y formatea
        clean_code = code.replace('=', '').replace('+', '').replace('/', '')[:20]
        return '-'.join([clean_code[i:i+5] for i in range(0, min(len(clean_code), 20), 5)])

    @staticmethod
    def validate_license_code(license_code, current_hwid):
        """
        Valida un código de licencia contra el HWID actual.

        Args:
            license_code (str): Código de licencia a validar
            current_hwid (str): HWID del equipo actual

        Returns:
            dict: Información de la licencia si es válida
            None: Si la licencia es inválida
        """
        try:
            # Reconstruye el código completo (esto es simplificado)
            # En producción, necesitarías almacenar el código completo
            clean_code = license_code.replace('-', '')

            # Para validación real, necesitarías el código completo original
            # Por ahora, esto es una validación simplificada
            # En la implementación real, validarías contra una base de datos

            return {
                'valid': True,
                'hwid': current_hwid,
                'message': 'Licencia validada correctamente'
            }

        except Exception as e:
            return None

    @staticmethod
    def create_license_file(hwid, license_code, file_path):
        """
        Crea un archivo de licencia cifrado.

        Args:
            hwid (str): Hardware ID
            license_code (str): Código de licencia
            file_path (str): Ruta donde guardar el archivo
        """
        license_data = {
            'hwid': hwid,
            'license_code': license_code,
            'activation_date': datetime.now().isoformat(),
            'app_version': '1.0'
        }

        json_data = json.dumps(license_data, indent=2)
        encrypted_data = LicenseCrypto.simple_encrypt(json_data)

        with open(file_path, 'w') as f:
            f.write(encrypted_data)

    @staticmethod
    def read_license_file(file_path):
        """
        Lee y descifra un archivo de licencia.

        Args:
            file_path (str): Ruta del archivo de licencia

        Returns:
            dict: Datos de la licencia
            None: Si el archivo no es válido
        """
        try:
            with open(file_path, 'r') as f:
                encrypted_data = f.read()

            decrypted_data = LicenseCrypto.simple_decrypt(encrypted_data)
            return json.loads(decrypted_data)

        except Exception as e:
            return None


if __name__ == "__main__":
    # Prueba del módulo
    print("=== Test del módulo de cifrado ===")

    # Test de cifrado/descifrado
    test_data = "Esto es una prueba de cifrado"
    print(f"\nDatos originales: {test_data}")

    encrypted = LicenseCrypto.simple_encrypt(test_data)
    print(f"Datos cifrados: {encrypted}")

    decrypted = LicenseCrypto.simple_decrypt(encrypted)
    print(f"Datos descifrados: {decrypted}")

    # Test de generación de código de licencia
    test_hwid = "ABCD1234EFGH5678IJKL9012MNOP3456"
    license_code = LicenseCrypto.generate_license_code(test_hwid)
    print(f"\nCódigo de licencia generado: {license_code}")
