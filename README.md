[readme_conversor_webm_vp8_vp9_y_audio_ogg_opus_wav.md](https://github.com/user-attachments/files/35262489/readme_conversor_webm_vp8_vp9_y_audio_ogg_opus_wav.md)
# Conversor a WebM (VP8/VP9) y Audio (OGG/OPUS/WAV)

Herramienta de escritorio con interfaz gráfica en Python (`tkinter`) apoyada en **FFmpeg**, **FFprobe** y **FFplay** para convertir videos a **WebM** (VP8 / VP9 VBR) y convertir o previsualizar audio/video hacia **OGG (Vorbis)**, **OPUS** o **WAV (PCM 16-bit)**, con soporte multiidioma (**Español**, **English** y **Português (Brasil)**).

---

## Requisitos y preparación

- **Sistema operativo:** Windows (recomendado) o sistemas compatibles con Python 3 y `tkinter`.
- **Dependencias de Python:** utiliza únicamente librerías estándar de Python (`tkinter`, `subprocess`, `threading`, `urllib`, `zipfile`, `shutil`, etc.).
- **Ejecutables de FFmpeg:** el script busca `ffmpeg.exe`, `ffprobe.exe` y `ffplay.exe` junto al programa, en `PATH` o en rutas comunes (`C:\ffmpeg`, `Program Files`, etc.).
- **Instalación automática al iniciar:** si no detecta `ffmpeg.exe` y `ffprobe.exe`, el programa muestra un aviso para descargarlos e instalarlos automáticamente junto al script o ejecutable desde la web oficial / paquete *essentials*.

---

## Cómo usarlo

### 1. Iniciar el programa e idioma
1. Ejecuta el script o el ejecutable compilado.
2. En la esquina superior derecha, haz clic en **Language** para cambiar entre **Español**, **English** o **Português (Brasil)**.
3. Marca o desmarca la casilla superior para mostrar u ocultar la sección de conversión de audio/video a **OGG / OPUS / WAV**.

### 2. Convertir video a WebM (VP8 / VP9)
1. En **Video de entrada**, haz clic en **Agregar archivos** y selecciona tu video.
2. En **Nombre del archivo**, escribe el nombre deseado (si lo dejas vacío, tomará el nombre del archivo de entrada). Los resultados se guardan automáticamente en la carpeta `Output` junto al programa, agregando sufijos numéricos (` 1`, ` 2`, etc.) si ya existe un archivo con el mismo nombre.
3. Ajusta los **Parámetros VP8 / VP9 VBR**:
   - **Códec de video:** `VP8` o `VP9`.
   - **Bitrate VBR (kbps)**, **Maxrate**, **Bufsize** y **CRF (0-63)**.
   - **Máxima fidelidad visual (CRF bajo):** limita el CRF a un rango bajo (`0` a `4`) cuando está activada.
   - **Cambiar resolución a:** escala el video (por ejemplo, `240p` a `1080p`) usando `lanczos` y un realce suave (`unsharp`) al escalar hacia arriba.
   - **Cambiar fotograma (1-60):** fija un FPS entre `1` y `60`, o conserva los FPS/cuadros originales si está desactivada.
   - **Audio:** elige `libopus`, `libvorbis` o `none` (sin audio) y define el bitrate de audio.
   - **Audio sincronizado:** permite asignar un archivo externo de audio o video con audio ya sincronizado en lugar de usar la pista original del video.
4. Haz clic en **Convertir a WebM**, sigue el progreso en barra/porcentaje y al terminar se abrirá el archivo generado o la carpeta `Output`.

### 3. Convertir audio o video a OGG / OPUS / WAV
1. En el bloque de conversión de audio/video, haz clic en **Agregar audio/video** y elige el archivo fuente.
2. Usa **Reproducir / Detener** para escuchar una vista previa interna con `ffplay.exe` aplicando el refuerzo en dB y el limitador configurados.
3. Define el **Nombre salida**, el **Formato** (`OGG`, `OPUS` o `WAV`) y el **Bitrate**.
4. Ajusta **Refuerzo (dB)** (con campo numérico o deslizador) y marca **Anti-saturación (limiter)** si deseas limitar picos al subir ganancia.
5. Haz clic en **Convertir audio** para guardar el resultado en la carpeta `Output`.

---

## Qué hacer (Buenas prácticas)

- **Mantén `ffmpeg.exe`, `ffprobe.exe` y `ffplay.exe` actualizados y accesibles:** así aseguras compatibilidad con más códecs de entrada, cálculo preciso de duración/resolución y vista previa de audio.
- **Verifica la sincronización antes de usar "Audio sincronizado":** asegúrate de que el audio externo o el video de referencia ya estén alineados en tiempo antes de unirlos al WebM.
- **Usa `libopus` o un bitrate adecuado (al menos `64k` / `48k`+) si eliges `libvorbis`:** evita errores de codificación por bitrates demasiado bajos en Vorbis.
- **Activa `Anti-saturación (limiter)` al aplicar refuerzo positivo en dB:** ayuda a prevenir distorsión o recorte (*clipping*) cuando subes el volumen.
- **Revisa la carpeta `Output` con "Abrir carpeta Output":** ahí centraliza el programa todos los archivos convertidos y evita sobrescribir salidas previas gracias al renombrado automático.

---

## Lo que NO se debe hacer

- **No elijas un archivo de salida que apunte exactamente al mismo archivo de entrada:** el programa bloquea sobrescribir el origen sobre sí mismo para evitar pérdida de datos.
- **No introduzcas FPS fuera del rango permitido (`1` a `60`) ni valores de dB no numéricos:** el programa validará y rechazará entradas inválidas antes de iniciar FFmpeg.
- **No uses bitrates excesivamente bajos en `libvorbis` (como `30k`):** `libvorbis` no admite esos valores y provocará error.
- **No cierres bruscamente durante una descarga/instalación de FFmpeg sin revisar la carpeta del programa:** si se interrumpe a medias, vuelve a ejecutar o comprueba que `ffmpeg.exe` y `ffprobe.exe` estén completos.
- **No dependas de una pista de audio externa sin comprobar su duración o desfase:** si el audio externo no coincide con la duración o ritmo del video, el resultado final quedará desfasado.

---

## Notas para publicar en GitHub

- Incluye este archivo como `README.md` en la raíz de tu repositorio (puedes abrirlo, ajustarlo o guardarlo desde el Bloc de notas en codificación **UTF-8**).
- Evita subir archivos pesados innecesarios (como `.zip` temporales o carpetas de salida con videos grandes) añadiendo reglas en un `.gitignore` si solo quieres publicar el código fuente y la documentación.
