# 🏹 The Shadow Curse: La Aventura de Geralt

Bienvenido a **The Shadow Curse**, un juego de aventuras en 2D donde encarnarás a Geralt, un poderoso hechicero que debe derrotar al Señor Oscuro y liberar su tierra de la corrupción.  

## 🎮 Características del Juego
- 🌲 **Mundos oscuros y misteriosos**: Explora bosques malditos, castillos sombríos y mazmorras peligrosas.
- 🧙 **Sistema de hechizos**: Lanza hechizos de fuego y hielo para derrotar a los enemigos.
- 👾 **Enemigos variados**: Enfréntate a magos oscuros, gólems, dragones y fantasmas.
- 📜 **Historia profunda**: Vive una narrativa envolvente con misiones y desafíos únicos.
- 🎶 **Música inmersiva**: Banda sonora original con efectos de sonido impactantes.

## 🏗️ Estructura del Proyecto
```
The-Shadow-Curse/
│
├── assets/                # Recursos gráficos y de audio
│   ├── images/            # Imágenes y sprites
│   │   ├── backgrounds/   # Fondos de escenarios
│   │   ├── characters/    # Personajes y enemigos
│   │   ├── items/         # Objetos del juego
│   │   ├── ui/            # Elementos de la interfaz de usuario
│   ├── sounds/            # Sonidos del juego (hechizos, golpes, etc.)
│   ├── music/             # Música del juego
│   ├── fonts/             # Fuentes personalizadas
│
├── intro/                 # Introducción del juego
│   ├── intro_video.mp4    # Video introductorio (opcional)
│   ├── intro_story.txt    # Guion de la introducción
│
├── levels/                # Código de los niveles del juego
│   ├── level_1.py
│   ├── level_2.py
│   ├── level_3.py
│   ├── level_4.py
│
├── src/
│   ├── player.py              # Lógica del personaje Geralt
│   ├── enemies.py             # Código de los enemigos
│
├── main.py                # Archivo principal del juego
├── README.md              # Documentación del proyecto
├── requirements.txt       # Dependencias del proyecto
└── utils.py               # Funciones auxiliares
```

## 🔥 Cómo Jugar
1. **Instala las dependencias**:  
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecuta el juego**:  
   ```bash
   python main.py
   ```
3. Usa las **teclas de dirección** para moverte y las teclas `F` y `I` para lanzar hechizos de fuego e hielo.

## 📜 Historia del Juego
Geralt, un hechicero legendario, regresa a su tierra natal solo para encontrarla consumida por la oscuridad. El **Señor Oscuro** ha esparcido una maldición, transformando el bosque en un lugar sombrío y atrayendo criaturas malignas. Ahora, Geralt debe atravesar **cuatro niveles** peligrosos, enfrentarse a hordas de enemigos y finalmente desafiar al Señor Oscuro en su castillo para restaurar la paz.

## 🎨 Créditos
- **Desarrollador**: [Tu Nombre]
- **Música**: Composición original
- **Sprites**: Diseños personalizados

🎮 ¡Disfruta del juego y que la magia te acompañe! ✨
