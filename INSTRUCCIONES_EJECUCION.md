# 🚀 Cómo Ejecutar la Aplicación

## ✅ PROBLEMA DETECTADO Y SOLUCIONADO

El problema era que la ventana de activación no se mostraba al frente cuando ejecutabas `main.py`.

He corregido el código y creado launchers más robustos.

---

## 📌 FORMAS DE EJECUTAR LA APP

### **OPCIÓN 1: Usando el Launcher Mejorado (RECOMENDADO)**

**Doble clic en:**
```
RUN_APP.bat
```

Este archivo:
- ✅ Muestra mensajes de progreso
- ✅ Detecta errores claramente
- ✅ Mantiene la ventana abierta si hay error
- ✅ Ejecuta la aplicación correctamente

---

### **OPCIÓN 2: Desde PowerShell o CMD**

**Abre PowerShell/CMD en la carpeta del proyecto y ejecuta:**

```powershell
python run_app.py
```

Verás mensajes como:
```
======================================================================
 GESTIÓN COMERCIAL - INICIANDO
======================================================================

[1/3] Cargando módulos...
      ✓ Módulos cargados correctamente

[2/3] Verificando sistema de licencias...
      ⚠ La aplicación no está activada
      → Se mostrará la ventana de activación

[3/3] Iniciando aplicación...
======================================================================
```

Y luego se abrirá la ventana de activación.

---

### **OPCIÓN 3: Ejecutar Directamente main.py**

```powershell
python gestion_comercial\main.py
```

**NOTA**: Si no se muestra la ventana, verifica que estás en la carpeta correcta.

---

## 🔧 SCRIPTS DE PRUEBA

### **Test del Sistema de Activación**

Para probar solo el sistema de licencias:

```powershell
python test_activation.py
```

Este script:
1. Verifica que todos los módulos se importen correctamente
2. Genera tu HWID
3. Verifica el estado de la licencia
4. Muestra la ventana de activación

---

## ❓ SI LA VENTANA NO SE MUESTRA

Si ejecutas la app y solo ves la pantalla negra sin ventana:

1. **Verifica que Python esté instalado correctamente:**
   ```powershell
   python --version
   ```
   Debería mostrar: `Python 3.12.x` o similar

2. **Verifica que tkinter esté disponible:**
   ```powershell
   python -c "import tkinter; print('Tkinter OK')"
   ```
   Debería mostrar: `Tkinter OK`

3. **Ejecuta el test de activación:**
   ```powershell
   python test_activation.py
   ```

4. **Revisa si hay errores en la consola** cuando ejecutas `run_app.py`

---

## 🎯 PROCESO COMPLETO DE PRIMERA EJECUCIÓN

1. **Ejecuta la app:**
   - Doble clic en `RUN_APP.bat`
   - O ejecuta: `python run_app.py`

2. **Verás la ventana de activación:**
   - Título: "Activación de Licencia - Gestión Comercial"
   - Muestra tu HWID (identificador del equipo)
   - Tiene un campo para ingresar el código

3. **Copia tu HWID:**
   - Haz clic en el botón "Copiar" junto al HWID

4. **Genera un código de activación:**
   - Abre otro PowerShell/CMD
   - Ejecuta: `python tools\license_generator.py`
   - Selecciona opción 1
   - Pega el HWID que copiaste
   - Te dará un código como: `ABCDE-FGHIJ-KLMNO-PQRST`

5. **Ingresa el código en la ventana:**
   - Pega el código en el campo "Código de Activación"
   - Haz clic en "Activar Licencia"

6. **¡Listo!**
   - La app se desbloqueará
   - Se cerrará la ventana de activación
   - Se abrirá la aplicación principal

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### Test Rápido:

```powershell
# 1. Ejecutar test de activación
python test_activation.py

# 2. Si el test pasa, ejecutar la app
python run_app.py
```

---

## 📝 NOTAS IMPORTANTES

### Si Cierras la Ventana de Activación:
- La aplicación se cerrará
- Deberás ejecutarla nuevamente
- Es normal, es el comportamiento de seguridad

### Si Ya Activaste Anteriormente:
- La app NO volverá a pedir el código
- Se abrirá directamente la aplicación principal
- La licencia está guardada en: `%APPDATA%\GestionComercial\license.dat`

### Para Desactivar la Licencia (Testing):
```powershell
# Elimina el archivo de licencia
del %APPDATA%\GestionComercial\license.dat
```

Luego al ejecutar la app, volverá a pedir activación.

---

## ✅ CAMBIOS REALIZADOS

He corregido:

1. **`gestion_comercial/modules/activation/view.py`**:
   - Agregado `deiconify()`, `lift()`, `focus_force()`
   - Agregado `attributes('-topmost', True)` temporalmente
   - Ahora la ventana se muestra SIEMPRE al frente

2. **`gestion_comercial/main.py`**:
   - Agregado manejo de excepciones
   - Agregado `update()` antes de `wait_window()`
   - Muestra errores en consola si algo falla

3. **Creado `run_app.py`**:
   - Launcher robusto con mensajes de progreso
   - Muestra errores claramente
   - Mejor experiencia de usuario

4. **Creado `RUN_APP.bat`**:
   - Archivo batch para ejecutar con doble clic
   - Mantiene ventana abierta si hay error

5. **Creado `test_activation.py`**:
   - Script para probar solo el sistema de activación
   - Útil para debugging

---

## 🚀 PRUEBA AHORA

**Ejecuta:**
```powershell
python run_app.py
```

O **doble clic en**: `RUN_APP.bat`

**Deberías ver:**
1. Mensajes de inicio en consola
2. Ventana de activación que aparece al frente
3. Tu HWID mostrado

**¡Prueba y me cuentas cómo te va!**
