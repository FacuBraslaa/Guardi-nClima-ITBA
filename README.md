# GuardiánClima ITBA

GuardiánClima es una aplicación de consola desarrollada en Python como trabajo práctico integrador para la materia de Tecnología del ITBA. La idea fue construir algo que combine todo lo que vimos durante el año: programación en Python, consumo de APIs, manejo de datos, inteligencia artificial y conceptos de ciberseguridad.

La app permite registrarse, iniciar sesión, consultar el clima de cualquier ciudad del mundo en tiempo real, ver un historial personal de consultas, revisar estadísticas globales entre todos los usuarios, y recibir un consejo de vestimenta generado por IA según las condiciones climáticas del momento.

---

## ¿Qué hace cada parte?

| Módulo | Descripción |
|---|---|
| `main.py` | Punto de entrada. Maneja los dos menús: el de acceso y el principal |
| `autenticacion.py` | Registro e inicio de sesión con lectura/escritura de CSV |
| `validador_contrasena.py` | Valida que la contraseña cumpla criterios de seguridad |
| `clima.py` | Consulta a la API de OpenWeatherMap y muestra los datos |
| `historial.py` | Guarda y lee el historial global de consultas en CSV |
| `estadisticas.py` | Calcula estadísticas sobre el historial (ciudad más buscada, promedio de temperatura, etc.) |
| `consejo_ia.py` | Llama a la API de Google Gemini para generar un consejo de ropa |

Los archivos `usuarios_simulados.csv` e `historial_global.csv` se crean automáticamente la primera vez que se ejecuta la app.

---

## Requisitos previos

- Python 3.10 o superior
- Conexión a internet
- Una API key gratuita de [OpenWeatherMap](https://openweathermap.org/api)
- Una API key gratuita de [Google Gemini](https://aistudio.google.com/app/apikey)

---

## Cómo instalarlo y correrlo

### 1. Clonar el repositorio

```bash
git clone https://github.com/FacuBraslaa/Guardi-nClima-ITBA.git
cd Guardi-nClima-ITBA
```

### 2. Instalar las dependencias

Ejecutar el siguiente comando en la terminal para instalar todas las librerías necesarias:

```bash
pip3 install requests google-genai python-dotenv
```

| Librería | Para qué se usa |
|---|---|
| `requests` | Hacer llamadas HTTP a la API de OpenWeatherMap |
| `google-genai` | Conectarse a la API de Google Gemini (IA generativa) |
| `python-dotenv` | Leer las API keys desde el archivo `.env` automáticamente |

> Si `pip3` no funciona, probá con `pip install requests google-genai python-dotenv`

### 3. Configurar las API keys

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
OPENWEATHER_API_KEY=tu_clave_de_openweathermap
GEMINI_API_KEY=tu_clave_de_gemini
```

La app lo lee automáticamente al iniciarse. No hace falta configurar variables de entorno manualmente.

### 4. Ejecutar

```bash
python3 main.py
```

---

## Flujo de uso

Al abrir la app aparece el **Menú de Acceso**:

```
1. Iniciar sesión
2. Registrarse
3. Salir
```

Después de autenticarse, se accede al **Menú Principal**:

```
1. Consultar clima de una ciudad
2. Ver mi historial
3. Estadísticas globales
4. Consejo de vestimenta (IA)
5. Acerca de la aplicación
6. Cerrar sesión
```

La primera vez hay que registrarse (opción 2 del primer menú). Al registrarse exitosamente, la app inicia sesión de forma automática.

---

## Validación de contraseñas

Una de las cosas que más me interesó implementar fue la validación de contraseñas, que aplica conceptos de ciberseguridad vistos en el curso. Al registrarse, el sistema evalúa 5 criterios y exige que se cumplan **al menos 3**:

| Criterio | Requisito |
|---|---|
| Longitud | Mínimo 8 caracteres |
| Mayúscula | Al menos una letra mayúscula |
| Minúscula | Al menos una letra minúscula |
| Número | Al menos un dígito |
| Carácter especial | Al menos uno de `! @ # $ % & * ( ) , . ?` |

Si la contraseña no es suficientemente segura, la app indica exactamente qué criterios faltan y da la opción de intentarlo de nuevo sin tener que empezar el registro desde cero.

---

## Seguridad de contraseñas

Las contraseñas **no se guardan en texto plano**. Antes de escribirlas en el CSV, se les aplica **PBKDF2-HMAC-SHA256** con un salt aleatorio de 16 bytes generado por usuario y 200.000 iteraciones. En el archivo solo queda el salt y el hash resultante:

```
usuario,salt,contrasena
facu,1cc9bbfd...,c9d6324c...
```

Esto garantiza que aunque alguien acceda al CSV, no pueda recuperar las contraseñas originales. Este es el mismo principio que usan los sistemas reales, donde librerías como `bcrypt` o `Argon2` hacen exactamente esto pero con algoritmos más modernos.

---

## Conceptos del curso aplicados

Este proyecto integra contenido de los cinco bloques del curso:

| Bloque | Concepto aplicado |
|---|---|
| Python | Módulos, funciones, manejo de archivos CSV, excepciones, type hints |
| Inteligencia Artificial | API de Google Gemini para generación de texto (LLM) |
| Redes | Consumo de APIs REST con `requests`, manejo de códigos HTTP |
| Ciberseguridad | Validación de contraseñas por criterios, conciencia sobre hashing |
| Análisis de datos | Procesamiento de CSV, estadísticas con `collections.Counter` |
