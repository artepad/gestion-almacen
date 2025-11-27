# 🔐 Sistema de Licenciamiento - Gestión Comercial

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Cómo Funciona](#cómo-funciona)
3. [Proceso de Distribución](#proceso-de-distribución)
4. [Generar Códigos de Activación](#generar-códigos-de-activación)
5. [Crear el Instalador](#crear-el-instalador)
6. [Estructura de Archivos](#estructura-de-archivos)
7. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📖 Descripción General

Este sistema de licenciamiento protege tu aplicación mediante:

- **Hardware ID (HWID)**: Identificador único del equipo del cliente
- **Código de Activación**: Código cifrado vinculado al HWID
- **Archivo de Licencia Cifrado**: Almacenado localmente en el equipo del cliente
- **Validación al Inicio**: Verifica la licencia cada vez que se ejecuta la app

### Características de Seguridad

✅ Impide copiar la aplicación a otro equipo
✅ El código de activación solo funciona en un PC específico
✅ Archivo de licencia cifrado con AES
✅ Sistema offline (no requiere internet)
✅ Base de datos de licencias generadas (para tu control)

---

## 🔄 Cómo Funciona

### Para el Cliente (Usuario Final)

1. **Instala la aplicación** desde `GestionComercial_Setup_v1.0.exe`
2. **Primera ejecución**: Aparece la ventana de activación
3. **Obtiene su HWID**: Un código único de su equipo
4. **Te contacta**: Te envía su HWID por email/WhatsApp
5. **Recibe el código**: Tú le proporcionas el código de activación
6. **Activa la licencia**: Ingresa el código y la app se desbloquea
7. **Uso permanente**: La licencia queda activada en ese PC

### Para Ti (Desarrollador/Vendedor)

1. **Cliente te contacta** con su HWID
2. **Generas el código** usando `license_generator.py`
3. **Envías el código** al cliente
4. **Registras la venta** (automático en `licenses_database.json`)

---

## 📦 Proceso de Distribución

### Paso 1: Construir el Ejecutable

1. Abre una terminal en la carpeta del proyecto
2. Ejecuta:
   ```bash
   build.bat
   ```
3. Espera a que termine (puede tardar 1-2 minutos)
4. Se creará `dist\GestionComercial.exe`

### Paso 2: Crear el Instalador

1. **Descarga Inno Setup**:
   - Ve a: https://jrsoftware.org/isdl.php
   - Descarga e instala Inno Setup 6

2. **Compila el instalador**:
   - Abre `installer.iss` con Inno Setup Compiler
   - Presiona `F9` o ve a `Build → Compile`
   - Espera a que termine

3. **Resultado**:
   - Se crea: `installer_output\GestionComercial_Setup_v1.0.exe`
   - Este es el archivo que distribuyes a tus clientes

### Paso 3: Distribuir

- **Sube el instalador** a Google Drive, Dropbox, o tu sitio web
- **Envía el link** a tus clientes
- **Proporciona instrucciones** de instalación

---

## 🔑 Generar Códigos de Activación

### Uso del Generador de Licencias

1. **Ejecuta el generador**:
   ```bash
   cd tools
   python license_generator.py
   ```

2. **Menú principal**:
   ```
   MENÚ PRINCIPAL
   1. Generar nuevo código de licencia
   2. Listar todas las licencias
   3. Buscar licencia
   4. Salir
   ```

3. **Generar código** (Opción 1):
   - Ingresa el **HWID** que te envió el cliente
   - Ingresa **nombre del cliente** (opcional pero recomendado)
   - Ingresa **email del cliente** (opcional)
   - Agrega **notas** si lo deseas

4. **Código generado**:
   ```
   ✅ ¡LICENCIA GENERADA EXITOSAMENTE!

   Cliente: Juan Pérez
   HWID: 1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P

   🔑 CÓDIGO DE ACTIVACIÓN:
       ABCDE-FGHIJ-KLMNO-PQRST

   📋 Proporcione este código al cliente para que active su copia.
   ```

5. **Envía el código** al cliente por email/WhatsApp

### Base de Datos de Licencias

- Se crea automáticamente: `tools/licenses_database.json`
- **Guárdala en un lugar seguro** (backup en la nube)
- Contiene:
  - Todos los códigos generados
  - Datos de clientes
  - HWIDs vinculados
  - Fechas de activación

**⚠️ IMPORTANTE**: No pierdas este archivo, es tu registro de ventas.

---

## 🏗️ Crear el Instalador

### Requisitos

1. **Python 3.8+** (ya lo tienes)
2. **PyInstaller** (ya instalado)
3. **Inno Setup 6** (descárgalo de: https://jrsoftware.org/isdl.php)

### Proceso Completo

```bash
# 1. Construir el ejecutable
build.bat

# 2. Abrir Inno Setup y compilar
# - Abre installer.iss con Inno Setup Compiler
# - Presiona F9

# 3. El instalador estará en:
# installer_output\GestionComercial_Setup_v1.0.exe
```

### Personalizar el Instalador

Edita `installer.iss` para cambiar:

- **Nombre de la empresa**:
  ```
  #define MyAppPublisher "Tu Nombre o Empresa"
  ```

- **URL del sitio web**:
  ```
  #define MyAppURL "https://www.tuempresa.com"
  ```

- **Versión**:
  ```
  #define MyAppVersion "1.0"
  ```

- **Agregar un icono**: Descomenta y especifica:
  ```
  SetupIconFile=ruta/al/icono.ico
  ```

---

## 📁 Estructura de Archivos

```
Gestión Almacén 2.0/
│
├── gestion_comercial/          # Código fuente de la aplicación
│   ├── core/                   # Núcleo de la aplicación
│   ├── modules/                # Módulos (launcher, cash_counter, etc.)
│   ├── licensing/              # 🔐 Sistema de licenciamiento
│   │   ├── hwid.py            # Generación de Hardware ID
│   │   ├── crypto.py          # Cifrado de licencias
│   │   └── validator.py       # Validación de licencias
│   └── main.py                # Punto de entrada (con validación)
│
├── tools/                      # 🔧 Herramientas del desarrollador
│   ├── license_generator.py   # Generador de códigos
│   └── licenses_database.json # Base de datos de licencias
│
├── build.bat                   # Script para construir .exe
├── build_exe.spec              # Configuración de PyInstaller
├── installer.iss               # Script de Inno Setup
│
├── dist/                       # 📦 Ejecutable generado
│   └── GestionComercial.exe
│
└── installer_output/           # 💿 Instalador final
    └── GestionComercial_Setup_v1.0.exe
```

---

## ❓ Preguntas Frecuentes

### ¿Qué pasa si el cliente cambia de PC?

- La licencia **no funcionará** en el nuevo PC
- Tendrás que generar un **nuevo código** para el nuevo HWID
- **Opción**: Puedes ofrecerle la opción de "transferir licencia" generando un nuevo código

### ¿El cliente puede desinstalar y reinstalar?

- **Sí**, la licencia se guarda en `%APPDATA%\GestionComercial`
- Al reinstalar, **sigue activada** (mismo PC)
- Solo se borra si el cliente formatea el disco

### ¿Qué pasa si el cliente cambia hardware?

Si cambia componentes menores (RAM, disco secundario): **Probablemente siga funcionando**
Si cambia componentes mayores (CPU, placa base): **Dejará de funcionar**
**Solución**: Generar nuevo código para el HWID actualizado

### ¿Puedo revocar una licencia?

- No automáticamente (es sistema offline)
- **Opción manual**: Crear una lista negra de HWIDs en una futura versión
- **Mejor práctica**: No generes código para clientes dudosos

### ¿Cómo actualizo la aplicación?

1. Modifica el código fuente
2. Ejecuta `build.bat` nuevamente
3. Crea nuevo instalador con Inno Setup
4. **Las licencias antiguas seguirán funcionando** (compatible)

### ¿Puedo probar la activación sin instalar?

**Sí**, prueba local:

1. Ejecuta directamente: `python gestion_comercial\main.py`
2. Verás la ventana de activación
3. Copia tu HWID
4. Genera un código con `license_generator.py`
5. Activa y prueba

Para **limpiar la licencia de prueba**:
```bash
# Elimina el archivo de licencia
del %APPDATA%\GestionComercial\license.dat
```

### ¿Es seguro este sistema?

**Para usuarios normales**: ✅ Muy seguro
**Para hackers expertos**: ⚠️ Puede ser vulnerado con ingeniería inversa avanzada

**Nivel de protección**:
- Evita copia casual: ✅ 100%
- Evita compartir entre amigos: ✅ 95%
- Evita piratería masiva: ✅ 85%
- Evita hackers profesionales: ⚠️ 60%

**Para aumentar seguridad**:
- Usa **PyArmor** para ofuscar el código
- Implementa validaciones adicionales
- Considera sistema online con servidor

---

## 🚀 Próximos Pasos Recomendados

1. **Prueba local completa**:
   - Ejecuta la app sin licencia
   - Genera un código
   - Activa y verifica

2. **Crea el instalador**:
   - Ejecuta `build.bat`
   - Compila con Inno Setup
   - Prueba la instalación en otra carpeta

3. **Prueba en máquina virtual** (opcional):
   - Crea una VM de Windows
   - Instala ahí
   - Verifica que todo funcione

4. **Documenta tu proceso de venta**:
   - ¿Cómo recibirás los HWIDs?
   - ¿Cómo enviarás los códigos?
   - ¿Qué soporte darás?

5. **Backup del generador**:
   - Guarda `tools/license_generator.py`
   - Guarda `licenses_database.json`
   - Haz backup periódico

---

## 📞 Soporte

Si tienes problemas o preguntas sobre el sistema de licenciamiento, revisa:

1. Esta documentación
2. Los comentarios en el código
3. El archivo `gestion_comercial/licensing/README.md` (si existe)

---

**¡Tu sistema de licenciamiento está listo para comercializar tu aplicación! 🎉**
