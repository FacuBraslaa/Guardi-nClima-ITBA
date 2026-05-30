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

## Instalación de librerías

Ejecutar este comando en la terminal para instalar todas las dependencias:

```bash
pip3 install requests google-genai python-dotenv
```

> Si `pip3` no funciona, probá con `pip install requests google-genai python-dotenv`

| Librería | Para qué se usa |
|---|---|
| `requests` | Llamadas HTTP a la API de OpenWeatherMap |
| `google-genai` | Conexión a Google Gemini (es la versión actualizada de `google-generativeai`) |
| `python-dotenv` | Leer las API keys desde el archivo `.env` sin exponerlas en el código |

---

## Configuración de API Keys

La app necesita dos API keys para funcionar: una de OpenWeatherMap y otra de Google Gemini. Ambas son gratuitas.

**¿Dónde conseguirlas?**
- OpenWeatherMap: registrarse en [openweathermap.org](https://openweathermap.org/api) → ir a "My API Keys"
- Google Gemini: entrar a [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) → crear una key nueva

**¿Cómo configurarlas de forma segura?**

Las keys nunca deben estar escritas directamente en el código ni subirse al repositorio. Para eso se usa un archivo `.env` que se crea localmente y se agrega al `.gitignore`.

Crear un archivo llamado `.env` en la raíz del proyecto con este contenido:

```
OPENWEATHER_API_KEY=tu_clave_de_openweathermap
GEMINI_API_KEY=tu_clave_de_gemini
```

Este archivo ya está incluido en el `.gitignore`, así que nunca va a ser subido a GitHub aunque hagas `git push`. La app lo lee automáticamente al iniciarse usando `python-dotenv`.

---

## Cómo ejecutar la aplicación

```bash
python3 main.py
```

---

## Flujo de menús

### Menú de acceso (antes de iniciar sesión)

```
1. Iniciar sesión
2. Registrarse
3. Salir
```

- **Opción 1 – Iniciar sesión**: pedí usuario y contraseña. Si son incorrectos, podés volver a intentarlo sin salir del menú.
- **Opción 2 – Registrarse**: creás un usuario nuevo. La contraseña se valida en el momento y si no cumple los requisitos te explica qué le falta. Al registrarte exitosamente iniciás sesión de forma automática.
- **Opción 3 – Salir**: cierra la aplicación.

### Menú principal (después de iniciar sesión)

```
1. Consultar clima de una ciudad
2. Ver mi historial
3. Estadísticas globales
4. Consejo de vestimenta (IA)
5. Acerca de la aplicación
6. Cerrar sesión
```

- **Opción 1 – Consultar clima**: ingresás el nombre de una ciudad y la app consulta la API de OpenWeatherMap. Muestra temperatura, sensación térmica, humedad, viento y condición. La consulta queda guardada en el historial.
- **Opción 2 – Ver mi historial**: muestra todas las ciudades que consultaste con fecha, hora y temperatura del momento.
- **Opción 3 – Estadísticas globales**: muestra datos del historial de todos los usuarios: total de consultas, ciudad más buscada y temperatura promedio.
- **Opción 4 – Consejo de vestimenta (IA)**: usa los datos de una ciudad de tu historial y llama a la API de Google Gemini para generar un consejo de qué ropa ponerse.
- **Opción 5 – Acerca de la aplicación**: muestra información sobre la app, tecnologías usadas y el sistema de seguridad de contraseñas.
- **Opción 6 – Cerrar sesión**: vuelve al menú de acceso.

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
