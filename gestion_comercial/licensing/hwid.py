"""
Módulo para generar Hardware ID (HWID) único del equipo.
Este ID se utiliza para vincular la licencia a un PC específico.
"""

import platform
import subprocess
import hashlib
import uuid


class HardwareID:
    """Clase para generar y validar Hardware IDs únicos."""

    @staticmethod
    def get_cpu_id():
        """Obtiene el ID del procesador."""
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output(
                    "wmic cpu get ProcessorId",
                    shell=True
                ).decode()
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    return lines[1].strip()
        except:
            pass
        return "UNKNOWN_CPU"

    @staticmethod
    def get_motherboard_id():
        """Obtiene el UUID de la placa base."""
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output(
                    "wmic baseboard get SerialNumber",
                    shell=True
                ).decode()
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    return lines[1].strip()
        except:
            pass
        return "UNKNOWN_MB"

    @staticmethod
    def get_machine_guid():
        """Obtiene el GUID de Windows (MachineGuid del registro)."""
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output(
                    'reg query "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
                    shell=True
                ).decode()
                for line in output.split('\n'):
                    if 'MachineGuid' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2].strip()
        except:
            pass
        return str(uuid.getnode())

    @staticmethod
    def get_disk_serial():
        """Obtiene el serial del disco duro principal."""
        try:
            if platform.system() == "Windows":
                output = subprocess.check_output(
                    "wmic diskdrive get SerialNumber",
                    shell=True
                ).decode()
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    serial = lines[1].strip()
                    if serial and serial != "":
                        return serial
        except:
            pass
        return "UNKNOWN_DISK"

    @staticmethod
    def generate_hwid():
        """
        Genera un Hardware ID único basado en componentes del hardware.

        Returns:
            str: Hardware ID en formato hexadecimal (32 caracteres)
        """
        # Recopila información del hardware
        cpu_id = HardwareID.get_cpu_id()
        mb_id = HardwareID.get_motherboard_id()
        machine_guid = HardwareID.get_machine_guid()
        disk_serial = HardwareID.get_disk_serial()

        # Combina todos los identificadores
        combined = f"{cpu_id}|{mb_id}|{machine_guid}|{disk_serial}"

        # Genera un hash SHA-256
        hwid_hash = hashlib.sha256(combined.encode()).hexdigest()

        return hwid_hash[:32].upper()  # Retorna los primeros 32 caracteres en mayúsculas

    @staticmethod
    def format_hwid(hwid):
        """
        Formatea el HWID en bloques de 4 caracteres para mejor legibilidad.

        Args:
            hwid (str): Hardware ID sin formato

        Returns:
            str: HWID formateado (ej: XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX)
        """
        return '-'.join([hwid[i:i+4] for i in range(0, len(hwid), 4)])

    @staticmethod
    def get_formatted_hwid():
        """
        Genera y formatea el HWID del equipo actual.

        Returns:
            str: HWID formateado
        """
        hwid = HardwareID.generate_hwid()
        return HardwareID.format_hwid(hwid)


# Función de conveniencia para uso directo
def get_hwid():
    """Retorna el HWID del equipo actual (sin formato)."""
    return HardwareID.generate_hwid()


def get_formatted_hwid():
    """Retorna el HWID del equipo actual (formateado)."""
    return HardwareID.get_formatted_hwid()


if __name__ == "__main__":
    # Prueba del módulo
    print("=== Test del módulo HWID ===")
    print(f"CPU ID: {HardwareID.get_cpu_id()}")
    print(f"Motherboard ID: {HardwareID.get_motherboard_id()}")
    print(f"Machine GUID: {HardwareID.get_machine_guid()}")
    print(f"Disk Serial: {HardwareID.get_disk_serial()}")
    print(f"\nHWID generado: {get_hwid()}")
    print(f"HWID formateado: {get_formatted_hwid()}")
