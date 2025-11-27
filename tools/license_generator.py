"""
Generador de Códigos de Licencia
=================================

Esta herramienta es para USO EXCLUSIVO DEL DESARROLLADOR.
Permite generar códigos de activación para los clientes.

USO:
    python license_generator.py

El cliente debe proporcionarte su HWID (que ve en la ventana de activación).
Tú ingresas ese HWID aquí y el sistema genera un código de activación.
"""

import sys
import os
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gestion_comercial.licensing.crypto import LicenseCrypto


class LicenseGenerator:
    """Generador de licencias para administradores."""

    LICENSE_DB_FILE = "licenses_database.json"

    def __init__(self):
        """Inicializa el generador."""
        self.load_database()

    def load_database(self):
        """Carga la base de datos de licencias generadas."""
        if os.path.exists(self.LICENSE_DB_FILE):
            with open(self.LICENSE_DB_FILE, 'r') as f:
                self.database = json.load(f)
        else:
            self.database = {
                "licenses": [],
                "created": datetime.now().isoformat()
            }

    def save_database(self):
        """Guarda la base de datos de licencias."""
        with open(self.LICENSE_DB_FILE, 'w') as f:
            json.dump(self.database, f, indent=2)

    def generate_license(self, hwid, customer_name="", customer_email="", notes=""):
        """
        Genera un código de licencia para un HWID específico.

        Args:
            hwid (str): Hardware ID del cliente
            customer_name (str): Nombre del cliente (opcional)
            customer_email (str): Email del cliente (opcional)
            notes (str): Notas adicionales (opcional)

        Returns:
            str: Código de licencia generado
        """
        # Limpiar HWID (quitar guiones si los tiene)
        clean_hwid = hwid.replace('-', '').strip().upper()

        # Verificar que el HWID tenga la longitud correcta
        if len(clean_hwid) != 32:
            raise ValueError(f"HWID inválido. Debe tener 32 caracteres, tiene {len(clean_hwid)}")

        # Generar código de licencia
        license_code = LicenseCrypto.generate_license_code(
            clean_hwid,
            product_name="GestionComercial",
            validity_days=36500  # 100 años (perpetua)
        )

        # Guardar en la base de datos
        license_record = {
            "hwid": clean_hwid,
            "license_code": license_code,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "notes": notes,
            "generated_date": datetime.now().isoformat(),
            "status": "active"
        }

        self.database["licenses"].append(license_record)
        self.save_database()

        return license_code

    def list_licenses(self):
        """Lista todas las licencias generadas."""
        if not self.database["licenses"]:
            print("\nNo hay licencias generadas aún.")
            return

        print("\n" + "=" * 80)
        print("LICENCIAS GENERADAS")
        print("=" * 80)

        for i, lic in enumerate(self.database["licenses"], 1):
            print(f"\n[{i}] Licencia #{i}")
            print(f"    Cliente: {lic.get('customer_name', 'N/A')}")
            print(f"    Email: {lic.get('customer_email', 'N/A')}")
            print(f"    HWID: {lic['hwid'][:16]}...{lic['hwid'][-16:]}")
            print(f"    Código: {lic['license_code']}")
            print(f"    Fecha: {lic['generated_date'][:10]}")
            print(f"    Estado: {lic['status']}")
            if lic.get('notes'):
                print(f"    Notas: {lic['notes']}")

        print("\n" + "=" * 80)

    def search_license(self, search_term):
        """Busca licencias por nombre, email o HWID."""
        search_term = search_term.lower()
        results = []

        for lic in self.database["licenses"]:
            if (search_term in lic.get('customer_name', '').lower() or
                search_term in lic.get('customer_email', '').lower() or
                search_term in lic['hwid'].lower()):
                results.append(lic)

        if not results:
            print(f"\nNo se encontraron licencias para: {search_term}")
            return

        print(f"\n{'=' * 80}")
        print(f"RESULTADOS DE BÚSQUEDA: '{search_term}'")
        print("=" * 80)

        for i, lic in enumerate(results, 1):
            print(f"\n[{i}]")
            print(f"    Cliente: {lic.get('customer_name', 'N/A')}")
            print(f"    Email: {lic.get('customer_email', 'N/A')}")
            print(f"    HWID: {lic['hwid']}")
            print(f"    Código: {lic['license_code']}")
            print(f"    Fecha: {lic['generated_date'][:10]}")

        print("\n" + "=" * 80)


def main():
    """Función principal del generador."""
    print("=" * 80)
    print("GENERADOR DE CÓDIGOS DE LICENCIA - GESTIÓN COMERCIAL")
    print("=" * 80)
    print("\nHerramienta para uso exclusivo del desarrollador")
    print("Versión 1.0\n")

    generator = LicenseGenerator()

    while True:
        print("\n" + "-" * 80)
        print("MENÚ PRINCIPAL")
        print("-" * 80)
        print("1. Generar nuevo código de licencia")
        print("2. Listar todas las licencias")
        print("3. Buscar licencia")
        print("4. Salir")
        print("-" * 80)

        choice = input("\nSeleccione una opción [1-4]: ").strip()

        if choice == "1":
            # Generar nueva licencia
            print("\n" + "=" * 80)
            print("GENERAR NUEVA LICENCIA")
            print("=" * 80)

            hwid = input("\nIngrese el HWID del cliente: ").strip()

            if not hwid:
                print("❌ Error: HWID no puede estar vacío")
                continue

            customer_name = input("Nombre del cliente (opcional): ").strip()
            customer_email = input("Email del cliente (opcional): ").strip()
            notes = input("Notas adicionales (opcional): ").strip()

            try:
                license_code = generator.generate_license(
                    hwid,
                    customer_name,
                    customer_email,
                    notes
                )

                print("\n" + "=" * 80)
                print("✅ ¡LICENCIA GENERADA EXITOSAMENTE!")
                print("=" * 80)
                print(f"\nCliente: {customer_name or 'N/A'}")
                print(f"HWID: {hwid}")
                print(f"\n🔑 CÓDIGO DE ACTIVACIÓN:")
                print(f"    {license_code}")
                print("\n" + "=" * 80)
                print("\n📋 Proporcione este código al cliente para que active su copia.")

            except ValueError as e:
                print(f"\n❌ Error: {e}")

        elif choice == "2":
            # Listar licencias
            generator.list_licenses()

        elif choice == "3":
            # Buscar licencia
            search_term = input("\nIngrese término de búsqueda (nombre/email/HWID): ").strip()
            if search_term:
                generator.search_license(search_term)
            else:
                print("❌ Término de búsqueda vacío")

        elif choice == "4":
            # Salir
            print("\n¡Hasta luego!")
            break

        else:
            print("\n❌ Opción inválida. Por favor seleccione 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
        sys.exit(0)
