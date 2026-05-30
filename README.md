# GuardiánClima ITBA

Aplicación de consola en Python que permite consultar el clima en tiempo real, gestionar usuarios, registrar un historial de consultas y recibir consejos de vestimenta generados por Inteligencia Artificial.

---

## Características

- Registro e inicio de sesión de usuarios con validación de contraseña
- Consulta del clima en tiempo real mediante la API de OpenWeatherMap
- Historial personal de consultas guardado en CSV
- Estadísticas globales: ciudad más consultada, temperatura promedio y usuarios únicos
- Consejos de vestimenta generados por Google Gemini según las condiciones climáticas
- Sección "Acerca de" con nota educativa sobre seguridad de contraseñas

---

## Estructura del proyecto

```
GuardiánClima-ITBA/
├── main.py                  # Punto de entrada y menús
├── autenticacion.py         # Login y registro de usuarios
├── validador_contrasena.py  # Validación de seguridad de contraseñas
├── clima.py                 # Consulta a la API de OpenWeatherMap
├── historial.py             # Lectura y escritura del historial global
├── estadisticas.py          # Estadísticas calculadas sobre el historial
├── consejo_ia.py            # Consejos de vestimenta via Google Gemini
├── usuarios_simulados.csv   # Base de datos de usuarios (generado automáticamente)
├── historial_global.csv     # Historial de consultas (generado automáticamente)
└── README.md
```

---

## Requisitos

- Python 3.10 o superior
- Conexión a internet
- Clave de API de [OpenWeatherMap](https://openweathermap.org/api) (gratuita)
- Clave de API de [Google Gemini](https://aistudio.google.com/app/apikey) (gratuita)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/FacuBraslaa/Guardi-nClima-ITBA.git
cd Guardi-nClima-ITBA
```

### 2. Instalar dependencias

```bash
pip install requests google-generativeai
```

### 3. Configurar las API keys

Las claves se leen desde variables de entorno. Configurarlas antes de ejecutar:

**En Linux/macOS:**
```bash
export OPENWEATHER_API_KEY="tu_clave_openweather"
export GEMINI_API_KEY="tu_clave_gemini"
```

**En Windows (CMD):**
```cmd
set OPENWEATHER_API_KEY=tu_clave_openweather
set GEMINI_API_KEY=tu_clave_gemini
```

**En Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="tu_clave_openweather"
$env:GEMINI_API_KEY="tu_clave_gemini"
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## Flujo de la aplicación

```
Menú de Acceso
├── 1. Iniciar sesión
├── 2. Registrarse
├── 3. Acerca de la aplicación
└── 4. Salir

Menú Principal (post-login)
├── 1. Consultar clima de una ciudad
├── 2. Ver mi historial
├── 3. Estadísticas globales
├── 4. Consejo de vestimenta (IA)
└── 5. Cerrar sesión
```

---

## Validación de contraseñas

Al registrarse, la contraseña debe cumplir **al menos 3** de los siguientes 5 criterios:

| Criterio | Requisito |
|---|---|
| Longitud | Mínimo 8 caracteres |
| Mayúscula | Al menos una letra mayúscula |
| Minúscula | Al menos una letra minúscula |
| Número | Al menos un dígito |
| Carácter especial | Al menos uno de `! @ # $ % & * ( ) , . ?` |

Si la contraseña no es válida, el sistema indica qué criterios no se cumplen y ofrece sugerencias para mejorarla.

---

## Nota de seguridad

Las contraseñas se almacenan en **texto plano** dentro de `usuarios_simulados.csv`. Esto es intencional con fines **educativos** para simplificar la implementación.

En un sistema real, las contraseñas nunca deben guardarse en texto plano. La práctica recomendada es aplicar un algoritmo de **hashing con salt**, como `bcrypt` o `Argon2`, de modo que incluso si la base de datos es comprometida, las contraseñas originales no puedan ser recuperadas.

---

## Tecnologías y conceptos aplicados

| Área | Concepto |
|---|---|
| Python | Módulos, funciones, manejo de archivos, excepciones |
| Redes | Consumo de APIs REST con `requests`, códigos HTTP |
| IA | Generación de texto con Google Gemini (LLM) |
| Ciberseguridad | Validación de contraseñas, hashing, almacenamiento seguro |
| Análisis de datos | Procesamiento de CSV, estadísticas con `collections.Counter` |
