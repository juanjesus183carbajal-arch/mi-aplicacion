EDUPLAY - PROYECTO FINAL POR PAGINAS

INSTALACIÓN
1. Instala Python 3 en Windows.
2. Descomprime EduPlay_Proyecto_Final.zip.
3. Abre la carpeta EduPlay_Proyecto_Final.
4. Ejecuta INICIAR_EDUPLAY.bat.
5. Abre http://127.0.0.1:5000.
6. Crea una cuenta y entra.

FUNCIONAMIENTO
- Solo hay dos materias: Lengua y Matemáticas.
- Cada materia abre su propia página.
- Cada tema abre una página de explicación con pasos, ejemplo y video relacionado.
- El botón "Comprueba lo aprendido" abre OTRA página con su actividad.
- Juegos separados por materia: memorama de conceptos y reto de palabras/cálculo.
- Examen separado para cada materia, con resultado y porcentaje.
- Registro, inicio de sesión, base de datos SQLite, puntos y progreso.

RUTAS DE IMÁGENES
Guarda tus imágenes dentro de static/img con estos nombres exactos:
- fondo-inicio.jpg
- fondo-lengua.jpg
- fondo-matematicas.jpg
- fondo-juegos.jpg
- fondo-examen.jpg
- logo-edupaly.png

Las rutas desde CSS/HTML son:
- static/img/fondo-inicio.jpg
- static/img/fondo-lengua.jpg
- static/img/fondo-matematicas.jpg
- static/img/fondo-juegos.jpg
- static/img/fondo-examen.jpg
- static/img/logo-edupaly.png

Los archivos .REEMPLAZAR.txt son recordatorios: bórralos cuando agregues la imagen real.
Para cambiar la imagen, conserva exactamente el nombre y extensión que usa la ruta.

NOTA
Los botones de video abren búsquedas de videos educativos de cada tema en YouTube.
El examen guarda los puntos de las respuestas correctas. El memorama y los retos son juegos de práctica en el navegador.
Para detener Flask, presiona CTRL+C en la ventana de la terminal.
