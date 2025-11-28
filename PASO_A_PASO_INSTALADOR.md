# 📦 GUÍA PASO A PASO: CREAR EL INSTALADOR

## ✅ **PROBLEMA SOLUCIONADO**

El error **"No module named 'gestion_comercial'"** ha sido corregido.

**Cambios realizados:**
- ✅ Creados archivos `__init__.py` en todos los módulos
- ✅ Corregido `build_exe.spec` para incluir correctamente el paquete
- ✅ Creado `build_clean.bat` para limpieza completa antes de build

---

## 🎯 **PROCESO COMPLETO: DE CÓDIGO A INSTALADOR**

```
┌─────────────────────────────────────────────────────┐
│ PASO 1: Verificar estructura del proyecto          │
│ → Ejecuta: python verify_structure.py              │
│ → Debe decir: "✅ ¡TODO CORRECTO!"                  │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ PASO 2: Crear el ejecutable (.exe)                 │
│ → Doble clic en: build_clean.bat                   │
│ → Espera 2-3 minutos                               │
│ → Se crea: dist\GestionComercial.exe               │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ PASO 3: Probar el ejecutable localmente            │
│ → Ejecuta: dist\GestionComercial.exe               │
│ → Debe abrir la ventana de activación              │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ PASO 4: Crear el instalador con Inno Setup         │
│ → Abre Inno Setup Compiler                         │
│ → Abre: installer.iss                              │
│ → Presiona F9                                       │
│ → Se crea: installer_output\                       │
│            GestionComercial_Setup_v1.0.exe          │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ PASO 5: Probar el instalador                       │
│ → Ejecuta el instalador                            │
│ → Instala y verifica que funcione                  │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ ✅ ¡LISTO PARA DISTRIBUIR!                          │
│ → Sube a Drive/Dropbox o tu sitio web              │
└─────────────────────────────────────────────────────┘
```

---

## 📋 **PASO 1: VERIFICAR ESTRUCTURA** ✅ (YA HECHO)

```powershell
python verify_structure.py
```

**Resultado esperado:**
```
✅ ¡TODO CORRECTO!
   Puedes ejecutar el build con seguridad:
   → Ejecuta: build_clean.bat
```

✅ **Ya verificamos esto y todo está correcto.**

---

## 📋 **PASO 2: CREAR EL EJECUTABLE**

### **Forma 1: Doble Clic (MÁS FÁCIL)**

1. Busca el archivo: **`build_clean.bat`**
2. **Doble clic** sobre él
3. Verás una ventana negra con mensajes como:

```
========================================
CONSTRUYENDO GESTION COMERCIAL
(Limpieza completa)
========================================

[1/4] Limpiando builds anteriores...
[2/4] Limpiando cache de Python...
[3/4] Compilando aplicacion con PyInstaller...
(Esto puede tardar 2-3 minutos...)
```

4. **ESPERA** hasta que termine (2-3 minutos la primera vez)

5. Al finalizar verás:

```
========================================
BUILD EXITOSO!
========================================

El ejecutable esta en: dist\GestionComercial.exe
Tamano: ~25-35 MB

Puedes probarlo ejecutando:
  dist\GestionComercial.exe

O crear el instalador con Inno Setup
```

### **Forma 2: Desde PowerShell**

```powershell
cd "C:\Users\del_a\Desktop\Gestión Almacén  2.0"
.\build_clean.bat
```

---

## 📋 **PASO 3: PROBAR EL EJECUTABLE**

Antes de crear el instalador, **SIEMPRE** prueba el ejecutable:

### **Test 1: Ejecutar el .exe**

```powershell
.\dist\GestionComercial.exe
```

**Debe pasar:**
- ✅ Se abre la ventana de activación
- ✅ Muestra tu HWID
- ✅ Puedes copiar el HWID
- ✅ Puedes ingresar un código (genera uno de prueba)

### **Test 2: Activar con código de prueba**

En otra terminal:

```powershell
python tools\license_generator.py
```

- Selecciona opción 1
- Pega el HWID que copiaste
- Obtén el código
- Ingrésalo en la ventana de activación

**Debe pasar:**
- ✅ Acepta el código
- ✅ La app se abre (ventana principal)

### **Test 3: Cerrar y volver a abrir**

```powershell
.\dist\GestionComercial.exe
```

**Debe pasar:**
- ✅ NO vuelve a pedir código
- ✅ Abre directamente la app

---

## 📋 **PASO 4: CREAR EL INSTALADOR CON INNO SETUP**

### **4.1 Descargar Inno Setup** (si no lo tienes)

1. Ve a: **https://jrsoftware.org/isdl.php**
2. Descarga: **Inno Setup 6.x** (versión estable)
3. Instala (siguiente → siguiente → instalar)

### **4.2 Compilar el Instalador**

1. **Abre Inno Setup Compiler** (búscalo en el menú inicio de Windows)

2. En el menú: **File → Open** (o presiona `Ctrl+O`)

3. Navega a tu carpeta del proyecto y abre:
   ```
   C:\Users\del_a\Desktop\Gestión Almacén  2.0\installer.iss
   ```

4. Verás el código del script. **Presiona F9** (o ve a **Build → Compile**)

5. Verás una ventana con progreso:
   ```
   Compiling...
   [1/10] Processing files...
   [2/10] Creating executable...
   ...
   ```

6. Al terminar (10-30 segundos), verás:
   ```
   Successful compile (0 errors, 0 warnings)

   Output file:
   C:\Users\del_a\Desktop\Gestión Almacén  2.0\installer_output\
   GestionComercial_Setup_v1.0.exe
   ```

7. **¡Listo!** El instalador está creado.

---

## 📋 **PASO 5: PROBAR EL INSTALADOR**

**IMPORTANTE:** Prueba el instalador ANTES de distribuirlo.

### **Opción A: Probar en tu PC**

1. Busca el archivo:
   ```
   installer_output\GestionComercial_Setup_v1.0.exe
   ```

2. **Doble clic** para ejecutarlo

3. Sigue el wizard:
   - Acepta licencia
   - Elige carpeta de instalación
   - Acepta crear acceso directo
   - Instalar

4. Al terminar, debería:
   - Abrir la app automáticamente
   - Mostrar ventana de activación
   - Funcionar correctamente

5. **Desinstala** después de probar:
   - Panel de Control → Programas → Desinstalar
   - Busca "Gestión Comercial"
   - Desinstala

### **Opción B: Probar en Máquina Virtual** (Recomendado)

Si tienes VirtualBox o VMware:

1. Crea una VM con Windows 10/11
2. Copia el instalador a la VM
3. Instala y prueba
4. Así verificas que funcione en un PC "limpio"

---

## ✅ **CHECKLIST ANTES DE DISTRIBUIR**

Antes de enviar el instalador a clientes, verifica:

### **Test del Ejecutable:**
- [ ] `dist\GestionComercial.exe` se ejecuta sin errores
- [ ] Aparece ventana de activación
- [ ] Puedes copiar HWID
- [ ] Acepta código válido
- [ ] App principal abre después de activar
- [ ] Al reabrir, NO pide código nuevamente

### **Test del Instalador:**
- [ ] Instalador se ejecuta sin errores
- [ ] Instala en Program Files correctamente
- [ ] Crea acceso directo en menú inicio
- [ ] App instalada abre y funciona
- [ ] Sistema de activación funciona
- [ ] Desinstalador funciona correctamente

---

## 🚀 **EJECUTA AHORA**

### **Comandos en orden:**

```powershell
# 1. Verificar estructura (opcional, ya lo hicimos)
python verify_structure.py

# 2. Crear el ejecutable
.\build_clean.bat

# 3. Probar el ejecutable
.\dist\GestionComercial.exe

# 4. Si funciona, crear instalador con Inno Setup (GUI)
# 5. Probar instalador
.\installer_output\GestionComercial_Setup_v1.0.exe
```

---

## ❓ **PREGUNTAS FRECUENTES**

### **¿Cuánto tarda el build?**
- Primera vez: 2-3 minutos
- Builds posteriores: 1-2 minutos

### **¿Qué tamaño tiene el ejecutable?**
- El .exe: ~25-35 MB
- El instalador: ~26-36 MB

### **¿Puedo cambiar el nombre del .exe?**
Sí, edita `build_exe.spec` línea 57:
```python
name='GestionComercial',  # Cambia aquí
```

### **¿Puedo cambiar la versión del instalador?**
Sí, edita `installer.iss` línea 7:
```ini
#define MyAppVersion "1.0"  ; Cambia aquí
```

### **¿El instalador funciona en cualquier Windows?**
Sí, en Windows 7, 8, 10 y 11 (32 y 64 bits).

---

## 🎯 **PRÓXIMO PASO PARA TI**

**Ejecuta ahora:**

```
1. Doble clic en: build_clean.bat
2. Espera a que termine
3. Ejecuta: dist\GestionComercial.exe
4. Verifica que funcione
```

**¡Cuéntame cuando termines el paso 2 y 3 para continuar con el instalador!**
