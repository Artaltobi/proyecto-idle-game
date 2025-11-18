# proyecto-idle-game

Cómo ejecutar el proyecto?
Para que el juego funcione, siempre debe ejecutarse desde dentro de la carpeta JUEGO_2.0, porque el código usa rutas relativas como:
      assets/images/...
Estas rutas solo existen cuando el programa se ejecuta desde esa carpeta.
Pasos correctos:
      cd JUEGO_2.0
      py main.py

🧵 Idle Factory – README Completo
🎮 ¿Qué es Idle Factory?

Idle Factory es un juego creado en Python + Pygame donde manejás un mundo con 3 fábricas:
🧦 Medias
🩳 Shorts
👕 Remeras
Podés caminar por un mapa estilo RPG, entrar a una fábrica y producir recursos para generar plata y mejorar tus edificios.
El juego está pensado con código simple, limpio y educativo.

🗺️ Overworld (Mapa)
Cuando iniciás el juego, aparecés en un mapa grande con un zoom dinámico.
Controles:
WASD → moverse
E → entrar a fábrica (si estás cerca)
ENTER → revivir si morís
ESC → volver atrás (en algunas pantallas)

💀 Cómo perder?
Hay una única forma de perder y es secreta
pista: Mojado
La pantalla se oscurece
Con ENTER respawneás en el centro del mapa

🏆 Cómo ganar
Ganás cuando:
✔ Las 3 fábricas están desbloqueadas
✔ Todas las fábricas tienen nivel 40+ (mesas doradas)
Al completar estos dos objetivos, aparece la pantalla de Victoria.

🏭 Sistema de Fábricas (dentro del edificio)
Esta parte es la más importante y es donde pasa “el juego de verdad”.
Todas las fábricas funcionan exactamente igual.
Cuando entrás a una fábrica, aparece un minijuego Idle donde producís, mejorás máquinas y ganás dinero.

🖱️ Cómo jugar dentro de la fábrica
✔️ Clickear mesas para producir
Cada mesa es una máquina.
Hacé click sobre la mesa para que empiece a producir.
Una barra avanza y cuando se llena → genera un producto.
Las mejorás con dinero y suben de nivel hasta nivel 40.
Cada nivel reduce el tiempo de producción y te da más plata.
Al llegar a nivel 40 se vuelven doradas (máxima eficiencia).
Este nivel cuenta para el progreso total del juego.

➤ Producción Manual (Tejedor)
Cuando clickeás una mesa, ayudás a avanzar su barra de producción.
Al completarse, generás productos.
También desde ahí podés mejorar la mesa.

➤ Economía y Dinero
Cada fábrica tiene un multiplicador distinto:
Medias → x1
Shorts → x2
Remeras → x3
Mejorar una mesa cuesta plata, y el costo sube a medida que aumenta el nivel.

➤ Vender Productos
Todo lo que producís se junta en un inventario.
Podés ir al Vendedor para vender todo y convertirlo en dinero.
El dinero se usa para:
mejorar mesas
desbloquear nuevas fábricas

➤ Desbloqueo de Fábricas
La fábrica 1 está desbloqueada desde el inicio.
Para acceder a las siguientes necesitás juntar cierta cantidad de dinero.
Cuando las desbloqueás, ya podés entrar desde el Overworld.
El fondo
Las imágenes de las mesas
La dificultad (x1, x2, x3 costos y ganancias)

