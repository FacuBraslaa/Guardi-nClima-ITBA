# GuardiánClima ITBA

Este es el TP integrador para la materia de Tecnología. La idea era hacer algo que juntara todo lo que fuimos viendo en el año, así que terminé haciendo una app de clima en consola que combina Python, APIs externas, manejo de archivos, seguridad y hasta inteligencia artificial.

Básicamente podés registrarte, iniciar sesión, consultar el clima de cualquier ciudad del mundo, ver tu historial de búsquedas, ver estadísticas de todos los usuarios y pedirle a una IA que te diga qué ropa ponerte según el clima de ese momento.

---

## Archivos del proyecto

- `main.py` — acá está todo el flujo de menús, es el punto de entrada
- `autenticacion.py` — maneja el registro y el login, lee y escribe el CSV de usuarios
- `validador_contrasena.py` — valida que la contraseña sea segura según criterios
- `clima.py` — hace las consultas a OpenWeatherMap y muestra los resultados
- `historial.py` — guarda y lee el historial de consultas en un CSV
- `estadisticas.py` — calcula estadísticas sobre el historial global
- `consejo_ia.py` — llama a la API de Gemini para generar el consejo de ropa

Los CSV se crean solos la primera vez que corrés la app, no hace falta crearlos a mano.

---

## Lo que necesitás para correrlo

- Python 3.10 o más nuevo
- Conexión a internet
- Una API key de OpenWeatherMap (es gratis, te registrás en openweathermap.org)
- Una API key de Google Gemini (también gratis, está en aistudio.google.com)

---

## Instalación

Primero cloná el repo:

```bash
git clone https://github.com/FacuBraslaa/Guardi-nClima-ITBA.git
cd Guardi-nClima-ITBA
```

Después instalás las dependencias:

```bash
pip3 install requests google-genai python-dotenv
```

Si `pip3` no te funciona probá con `pip` solo.

Las tres librerías que usa el proyecto son `requests` para llamar a la API del clima, `google-genai` para conectarse a Gemini y `python-dotenv` para leer las claves desde un archivo de configuración.

Después creás un archivo `.env` en la carpeta del proyecto con tus claves:

```
OPENWEATHER_API_KEY=tu_clave_aqui
GEMINI_API_KEY=tu_clave_aqui
```

Y ya podés correrlo con:

```bash
python3 main.py
```

---

## Cómo funciona

Cuando abrís la app te aparece el menú de inicio donde podés registrarte o iniciar sesión. La primera vez tenés que registrarte. Una vez adentro tenés acceso a todo:

```
1. Consultar clima de una ciudad
2. Ver mi historial
3. Estadísticas globales
4. Consejo de vestimenta (IA)
5. Acerca de la aplicación
6. Cerrar sesión
```

---

## Validación de contraseñas

Cuando te registrás, la contraseña tiene que cumplir al menos 3 de estos 5 criterios:

- 8 caracteres o más
- Una mayúscula
- Una minúscula  
- Un número
- Un carácter especial (!, @, #, etc.)

Si no cumple los requisitos la app te dice exactamente qué le falta y te deja intentarlo de nuevo.

---

## Seguridad

Las contraseñas no se guardan en texto plano. Antes de guardarlas en el CSV se hashean con PBKDF2-SHA256 usando un salt aleatorio distinto para cada usuario. Lo que queda en el archivo es el salt y el hash, nunca la contraseña original.

Lo implementé así porque en el bloque de ciberseguridad vimos que guardar contraseñas en texto plano es un problema grave. Si alguien accede al CSV no puede hacer nada con esos datos.

---

## Qué aplica de cada bloque

- **Python**: módulos, manejo de excepciones, archivos CSV, funciones
- **IA**: API de Google Gemini para generar texto con un modelo de lenguaje
- **Redes**: consumo de APIs REST, manejo de respuestas HTTP y errores de conexión
- **Ciberseguridad**: validación de contraseñas, hashing con salt
- **Análisis de datos**: estadísticas del historial usando `collections.Counter`
