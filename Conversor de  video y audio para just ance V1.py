import os
import re
import shutil
import subprocess
import sys
import threading
import tempfile
import tkinter as tk
import urllib.parse
import urllib.request
import zipfile
from tkinter import filedialog, messagebox, ttk


FFMPEG_OFFICIAL_PAGE = "https://ffmpeg.org/download.html"
FFMPEG_FALLBACK_ZIP_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

TRANSLATIONS = {
    "es": {
        "window_title": "Conversor a Webm (VP8/VP9) y Audio (OGG/OPUS/WAV)",
        "lang_button": "Language",
        "lang_es": "Español",
        "lang_en": "English",
        "lang_pt": "Português (Brasil)",
        "chk_show_audio_sec": "Apartado de conversión de audio y video a OGG / OPUS / WAV",
        "frm_in": "Video de entrada (cualquier códec)",
        "btn_add": "Agregar archivos",
        "frm_out": "Nombre del archivo (se guarda en la carpeta Output)",
        "lbl_name": "Nombre archivo:",
        "btn_open_out": "Abrir carpeta Output",
        "frm_cfg": "Parámetros VP8 / VP9 VBR",
        "lbl_codec": "Códec de video:",
        "lbl_bitrate": "Bitrate VBR (kbps):",
        "lbl_maxrate": "Maxrate:",
        "lbl_bufsize": "Bufsize:",
        "lbl_crf": "CRF (0-63):",
        "chk_fidelity": "Máxima fidelidad visual (CRF bajo)",
        "chk_resize": "Cambiar resolución a:",
        "res_off": "Desactivada: se mantiene el video original",
        "res_on": "Activa: escalado de detalle a {res}",
        "chk_fps": "Cambiar fotograma (1-60):",
        "fps_off": "Desactivada: FPS y cuadros originales",
        "fps_on": "Activa: {fps} fps",
        "fps_prompt": "Escribe un valor entre 1 y 60 fps",
        "lbl_audio": "Audio:",
        "lbl_abitrate": "Bitrate audio:",
        "btn_sync_audio": "Audio sincronizado",
        "sync_audio_none": "Audio del video original",
        "sync_audio_set": "Audio externo: {name}",
        "sync_audio_notice_title": "Audio sincronizado",
        "sync_audio_notice_msg": (
            "Aviso: el audio que elijas debe estar ya sincronizado con el video, "
            "ya sea mediante un audio editado en editores de video o usando el mismo "
            "video con audio si lo tienes para ponérselo.\n\n"
            "¿Deseas seleccionar ahora el archivo de audio o video con audio?"
        ),
        "sync_audio_dialog_title": "Seleccionar audio sincronizado o video con audio",
        "sync_audio_filter_media": "Audio y video",
        "sync_audio_filter_audio": "Archivos de audio",
        "sync_audio_filter_video": "Archivos de video",
        "sync_audio_filter_all": "Todos los archivos",
        "btn_convert": "Convertir a WebM",
        "frm_aud_conv": "Convertir audio y video a OGG / OPUS / WAV (cualquier códec)",
        "lbl_aud_in": "Audio/video entrada:",
        "btn_aud_add": "Agregar audio/video",
        "btn_aud_play": "Reproducir",
        "btn_aud_stop": "Detener",
        "lbl_aud_out": "Nombre salida:",
        "lbl_aud_fmt": "Formato:",
        "lbl_aud_br": "Bitrate:",
        "lbl_aud_db": "Refuerzo (dB):",
        "chk_aud_limiter": "Anti-saturación (limiter)",
        "btn_aud_convert": "Convertir audio",
        "aud_dialog_title": "Seleccionar archivo de audio o video con audio",
        "aud_warn_no_file_title": "Audio faltante",
        "aud_warn_no_file_msg": "Pulsa 'Agregar audio/video' y selecciona un archivo válido.",
        "aud_warn_db_title": "Decibelios no válidos",
        "aud_warn_db_msg": "Escribe un valor numérico de dB válido (por ejemplo 0, 3, 6.5 o 12).",
        "aud_no_ffplay_title": "Reproductor interno no disponible",
        "aud_no_ffplay_msg": "No se encontró ffplay.exe junto al programa. Instala FFmpeg desde el inicio para reproducir dentro del conversor.",
        "aud_preview_playing": "Reproduciendo vista previa en el conversor ({db_tag})...",
        "aud_preview_stopped": "Vista previa de audio detenida.",
        "aud_conv_prep": "Calculando duración y preparando conversión de audio...",
        "aud_conv_prog": "Convirtiendo audio a {fmt} ({bitrate}{db_tag})... {pct:.1f}%",
        "aud_conv_fin": "Finalizando archivo de audio...",
        "aud_conv_done": "Listo: audio guardado en {out_file}",
        "status_ready": "Listo. Los videos se guardarán en: {out_dir}",
        "status_detected": "FFmpeg y sus archivos detectados. Listo para convertir.",
        "status_no_ffmpeg": "Aviso: no tienes los archivos de FFmpeg instalados.",
        "dlg_no_ffmpeg_title": "FFmpeg no encontrado",
        "dlg_no_ffmpeg_msg": (
            "No tienes los archivos de FFmpeg instalados en tu equipo.\n\n"
            "¿Deseas descargar e instalar FFmpeg desde la página oficial ahora?"
        ),
        "btn_install": "Instalar",
        "btn_cancel": "Cancelar",
        "inst_start": "Iniciando instalación de FFmpeg... 5.0%",
        "inst_page": "Consultando página oficial de FFmpeg... 10.0%",
        "inst_connect": "Conectando con el servidor de descarga... 15.0%",
        "inst_dl": "Descargando FFmpeg ({mb:.1f} MB)... {pct:.1f}%",
        "inst_extract_start": "Instalando ejecutables de FFmpeg junto al programa... 76.0%",
        "inst_extract_file": "Instalando {name}... {pct:.1f}%",
        "inst_done": "FFmpeg y sus archivos instalados en: {app_dir} (100.0%)",
        "inst_missing_bins": "El paquete descargado no contenía ffmpeg.exe y ffprobe.exe.",
        "inst_err": "No se pudo descargar/instalar FFmpeg desde la web:\n{err}",
        "inst_done_title": "Instalación completada",
        "inst_err_title": "Error al instalar FFmpeg",
        "folder_opened": "Carpeta abierta: {out_dir}",
        "folder_err_title": "No se pudo abrir la carpeta",
        "folder_err_msg": "Error al abrir Output:\n{err}",
        "file_dialog_title": "Agregar archivo de video",
        "file_filter_video": "Archivos de video",
        "file_filter_all": "Todos los archivos",
        "dup_found": "Ya existía {name} en Output; se guardará como {final}.",
        "ready_save": "Listo para guardar en: {final}",
        "warn_no_file_title": "Archivo faltante",
        "warn_no_file_msg": "Pulsa 'Agregar archivos' y selecciona un video válido.",
        "warn_fps_title": "FPS fuera de rango",
        "warn_fps_msg": "La tasa de fotogramas debe ser un número entre 1 y 60 fps.",
        "warn_vorbis_title": "Bitrate de audio muy bajo para Vorbis",
        "warn_vorbis_msg": "libvorbis no admite bitrates tan bajos como 30k (error -22). Usa al menos 64k o cambia el audio a libopus.",
        "warn_same_title": "Mismo archivo",
        "warn_same_msg": "La entrada y la salida apuntan al mismo archivo. Cambia el nombre del archivo.",
        "conv_prep": "Calculando duración y preparando conversión VBR...",
        "conv_prog": "Convirtiendo a {codec}{res}{fps} ({bitrate} VBR)... {pct:.1f}%",
        "conv_fin": "Finalizando archivo WebM...",
        "conv_done": "Listo: guardado en {out_file}",
        "conv_err": "FFmpeg devolvió error:\n{err}",
        "conv_no_ff": "No se encontró ffmpeg.exe junto al script o ejecutable.",
        "conv_unexp": "Error inesperado: {err}",
        "conv_unknown": "Error desconocido en FFmpeg.",
        "conv_done_title": "Conversión completada",
        "conv_err_title": "Error en la conversión",
    },
    "en": {
        "window_title": "WebM Converter (VP8/VP9) & Audio (OGG/OPUS/WAV)",
        "lang_button": "Language",
        "lang_es": "Español",
        "lang_en": "English",
        "lang_pt": "Português (Brasil)",
        "chk_show_audio_sec": "Audio & video to OGG / OPUS / WAV conversion section",
        "frm_in": "Input video (any codec)",
        "btn_add": "Add files",
        "frm_out": "Output file name (saved in the Output folder)",
        "lbl_name": "File name:",
        "btn_open_out": "Open Output folder",
        "frm_cfg": "VP8 / VP9 VBR Parameters",
        "lbl_codec": "Video codec:",
        "lbl_bitrate": "VBR bitrate (kbps):",
        "lbl_maxrate": "Maxrate:",
        "lbl_bufsize": "Bufsize:",
        "lbl_crf": "CRF (0-63):",
        "chk_fidelity": "Maximum visual fidelity (low CRF)",
        "chk_resize": "Change resolution to:",
        "res_off": "Off: keeping original video resolution",
        "res_on": "Active: detail scaling to {res}",
        "chk_fps": "Change frame rate (1-60):",
        "fps_off": "Off: original FPS and frames",
        "fps_on": "Active: {fps} fps",
        "fps_prompt": "Enter a value between 1 and 60 fps",
        "lbl_audio": "Audio:",
        "lbl_abitrate": "Audio bitrate:",
        "btn_sync_audio": "Synced audio",
        "sync_audio_none": "Original video audio",
        "sync_audio_set": "External audio: {name}",
        "sync_audio_notice_title": "Synced audio",
        "sync_audio_notice_msg": (
            "Notice: the audio you choose must already be synced with the video, "
            "either via audio edited in video editors or by using the same video "
            "with audio if you have it to attach.\n\n"
            "Do you want to select the audio file or video with audio now?"
        ),
        "sync_audio_dialog_title": "Select synced audio or video with audio",
        "sync_audio_filter_media": "Audio and video",
        "sync_audio_filter_audio": "Audio files",
        "sync_audio_filter_video": "Video files",
        "sync_audio_filter_all": "All files",
        "btn_convert": "Convert to WebM",
        "frm_aud_conv": "Convert audio and video to OGG / OPUS / WAV (any codec)",
        "lbl_aud_in": "Input audio/video:",
        "btn_aud_add": "Add audio/video",
        "btn_aud_play": "Play",
        "btn_aud_stop": "Stop",
        "lbl_aud_out": "Output name:",
        "lbl_aud_fmt": "Format:",
        "lbl_aud_br": "Bitrate:",
        "lbl_aud_db": "Boost (dB):",
        "chk_aud_limiter": "Anti-clipping (limiter)",
        "btn_aud_convert": "Convert audio",
        "aud_dialog_title": "Select audio file or video with audio",
        "aud_warn_no_file_title": "Missing audio",
        "aud_warn_no_file_msg": "Click 'Add audio/video' and select a valid file.",
        "aud_warn_db_title": "Invalid decibels",
        "aud_warn_db_msg": "Enter a valid numeric dB value (for example 0, 3, 6.5 or 12).",
        "aud_no_ffplay_title": "Built-in player unavailable",
        "aud_no_ffplay_msg": "ffplay.exe was not found next to the program. Install FFmpeg on startup to play inside the converter.",
        "aud_preview_playing": "Playing audio preview in converter ({db_tag})...",
        "aud_preview_stopped": "Audio preview stopped.",
        "aud_conv_prep": "Calculating duration and preparing audio conversion...",
        "aud_conv_prog": "Converting audio to {fmt} ({bitrate}{db_tag})... {pct:.1f}%",
        "aud_conv_fin": "Finalizing audio file...",
        "aud_conv_done": "Done: audio saved to {out_file}",
        "status_ready": "Ready. Videos will be saved in: {out_dir}",
        "status_detected": "FFmpeg and its files detected. Ready to convert.",
        "status_no_ffmpeg": "Notice: FFmpeg files are not installed.",
        "dlg_no_ffmpeg_title": "FFmpeg not found",
        "dlg_no_ffmpeg_msg": (
            "You do not have FFmpeg files installed on your computer.\n\n"
            "Do you want to download and install FFmpeg from the official website now?"
        ),
        "btn_install": "Install",
        "btn_cancel": "Cancel",
        "inst_start": "Starting FFmpeg installation... 5.0%",
        "inst_page": "Checking official FFmpeg website... 10.0%",
        "inst_connect": "Connecting to download server... 15.0%",
        "inst_dl": "Downloading FFmpeg ({mb:.1f} MB)... {pct:.1f}%",
        "inst_extract_start": "Installing FFmpeg executables next to the program... 76.0%",
        "inst_extract_file": "Installing {name}... {pct:.1f}%",
        "inst_done": "FFmpeg and its files installed in: {app_dir} (100.0%)",
        "inst_missing_bins": "The downloaded package did not contain ffmpeg.exe and ffprobe.exe.",
        "inst_err": "Could not download/install FFmpeg from the web:\n{err}",
        "inst_done_title": "Installation complete",
        "inst_err_title": "FFmpeg installation error",
        "folder_opened": "Folder opened: {out_dir}",
        "folder_err_title": "Could not open folder",
        "folder_err_msg": "Error opening Output:\n{err}",
        "file_dialog_title": "Add video file",
        "file_filter_video": "Video files",
        "file_filter_all": "All files",
        "dup_found": "{name} already existed in Output; it will be saved as {final}.",
        "ready_save": "Ready to save to: {final}",
        "warn_no_file_title": "Missing file",
        "warn_no_file_msg": "Click 'Add files' and select a valid video.",
        "warn_fps_title": "FPS out of range",
        "warn_fps_msg": "Frame rate must be a number between 1 and 60 fps.",
        "warn_vorbis_title": "Audio bitrate too low for Vorbis",
        "warn_vorbis_msg": "libvorbis does not support bitrates as low as 30k (error -22). Use at least 64k or switch audio to libopus.",
        "warn_same_title": "Same file",
        "warn_same_msg": "Input and output point to the same file. Change the file name.",
        "conv_prep": "Calculating duration and preparing VBR conversion...",
        "conv_prog": "Converting to {codec}{res}{fps} ({bitrate} VBR)... {pct:.1f}%",
        "conv_fin": "Finalizing WebM file...",
        "conv_done": "Done: saved to {out_file}",
        "conv_err": "FFmpeg returned an error:\n{err}",
        "conv_no_ff": "ffmpeg.exe was not found next to the script or executable.",
        "conv_unexp": "Unexpected error: {err}",
        "conv_unknown": "Unknown FFmpeg error.",
        "conv_done_title": "Conversion complete",
        "conv_err_title": "Conversion error",
    },
    "pt": {
        "window_title": "Conversor para Webm (VP8/VP9) e Áudio (OGG/OPUS/WAV)",
        "lang_button": "Language",
        "lang_es": "Español",
        "lang_en": "English",
        "lang_pt": "Português (Brasil)",
        "chk_show_audio_sec": "Seção de conversão de áudio e vídeo para OGG / OPUS / WAV",
        "frm_in": "Vídeo de entrada (qualquer codec)",
        "btn_add": "Adicionar arquivos",
        "frm_out": "Nome do arquivo (salvo na pasta Output)",
        "lbl_name": "Nome arquivo:",
        "btn_open_out": "Abrir pasta Output",
        "frm_cfg": "Parâmetros VP8 / VP9 VBR",
        "lbl_codec": "Codec de vídeo:",
        "lbl_bitrate": "Bitrate VBR (kbps):",
        "lbl_maxrate": "Maxrate:",
        "lbl_bufsize": "Bufsize:",
        "lbl_crf": "CRF (0-63):",
        "chk_fidelity": "Máxima fidelidade visual (CRF baixo)",
        "chk_resize": "Alterar resolução para:",
        "res_off": "Desativada: mantém o vídeo original",
        "res_on": "Ativa: escala de detalhe em {res}",
        "chk_fps": "Alterar quadros (1-60):",
        "fps_off": "Desativada: FPS e quadros originais",
        "fps_on": "Ativa: {fps} fps",
        "fps_prompt": "Digite um valor entre 1 e 60 fps",
        "lbl_audio": "Áudio:",
        "lbl_abitrate": "Bitrate áudio:",
        "btn_sync_audio": "Áudio sincronizado",
        "sync_audio_none": "Áudio do vídeo original",
        "sync_audio_set": "Áudio externo: {name}",
        "sync_audio_notice_title": "Áudio sincronizado",
        "sync_audio_notice_msg": (
            "Aviso: o áudio escolhido já deve estar sincronizado com o vídeo, "
            "seja por meio de um áudio editado em editores de vídeo ou usando o "
            "mesmo vídeo com áudio caso você tenha para colocar.\n\n"
            "Deseja selecionar agora o arquivo de áudio ou vídeo com áudio?"
        ),
        "sync_audio_dialog_title": "Selecionar áudio sincronizado ou vídeo com áudio",
        "sync_audio_filter_media": "Áudio e vídeo",
        "sync_audio_filter_audio": "Arquivos de áudio",
        "sync_audio_filter_video": "Arquivos de vídeo",
        "sync_audio_filter_all": "Todos os arquivos",
        "btn_convert": "Converter para WebM",
        "frm_aud_conv": "Converter áudio e vídeo para OGG / OPUS / WAV (qualquer codec)",
        "lbl_aud_in": "Áudio/vídeo entrada:",
        "btn_aud_add": "Adicionar áudio/vídeo",
        "btn_aud_play": "Reproduzir",
        "btn_aud_stop": "Parar",
        "lbl_aud_out": "Nome saída:",
        "lbl_aud_fmt": "Formato:",
        "lbl_aud_br": "Bitrate:",
        "lbl_aud_db": "Reforço (dB):",
        "chk_aud_limiter": "Anti-saturação (limiter)",
        "btn_aud_convert": "Converter audio",
        "aud_dialog_title": "Selecionar arquivo de áudio ou vídeo com audio",
        "aud_warn_no_file_title": "Áudio ausente",
        "aud_warn_no_file_msg": "Clique em 'Adicionar áudio/vídeo' e selecione um arquivo válido.",
        "aud_warn_db_title": "Decibéis inválidos",
        "aud_warn_db_msg": "Digite um valor numérico de dB válido (por exemplo 0, 3, 6.5 ou 12).",
        "aud_no_ffplay_title": "Player interno indisponível",
        "aud_no_ffplay_msg": "ffplay.exe não foi encontrado ao lado do programa. Instale o FFmpeg na inicialização para tocar dentro do conversor.",
        "aud_preview_playing": "Reproduzindo prévia no conversor ({db_tag})...",
        "aud_preview_stopped": "Prévia de áudio interrompida.",
        "aud_conv_prep": "Calculando duração e preparando conversão de áudio...",
        "aud_conv_prog": "Convertendo áudio para {fmt} ({bitrate}{db_tag})... {pct:.1f}%",
        "aud_conv_fin": "Finalizando arquivo de áudio...",
        "aud_conv_done": "Concluído: áudio salvo em {out_file}",
        "status_ready": "Pronto. Os vídeos serão salvos em: {out_dir}",
        "status_detected": "FFmpeg e seus arquivos detectados. Pronto para converter.",
        "status_no_ffmpeg": "Aviso: os arquivos do FFmpeg não estão instalados.",
        "dlg_no_ffmpeg_title": "FFmpeg não encontrado",
        "dlg_no_ffmpeg_msg": (
            "Você não tem os arquivos do FFmpeg instalados no computador.\n\n"
            "Deseja baixar e instalar o FFmpeg a partir do site oficial agora?"
        ),
        "btn_install": "Instalar",
        "btn_cancel": "Cancelar",
        "inst_start": "Iniciando instalação do FFmpeg... 5.0%",
        "inst_page": "Consultando site oficial do FFmpeg... 10.0%",
        "inst_connect": "Conectando ao servidor de download... 15.0%",
        "inst_dl": "Baixando FFmpeg ({mb:.1f} MB)... {pct:.1f}%",
        "inst_extract_start": "Instalando executáveis do FFmpeg ao lado do programa... 76.0%",
        "inst_extract_file": "Instalando {name}... {pct:.1f}%",
        "inst_done": "FFmpeg e seus arquivos instalados em: {app_dir} (100.0%)",
        "inst_missing_bins": "O pacote baixado não continha ffmpeg.exe e ffprobe.exe.",
        "inst_err": "Não foi possível baixar/instalar o FFmpeg pela internet:\n{err}",
        "inst_done_title": "Instalação concluída",
        "inst_err_title": "Erro ao instalar FFmpeg",
        "folder_opened": "Pasta aberta: {out_dir}",
        "folder_err_title": "Não foi possível abrir a pasta",
        "folder_err_msg": "Erro ao abrir Output:\n{err}",
        "file_dialog_title": "Adicionar arquivo de vídeo",
        "file_filter_video": "Arquivos de vídeo",
        "file_filter_all": "Todos os arquivos",
        "dup_found": "{name} já existia em Output; será salvo como {final}.",
        "ready_save": "Pronto para salvar em: {final}",
        "warn_no_file_title": "Arquivo ausente",
        "warn_no_file_msg": "Clique em 'Adicionar arquivos' e selecione um vídeo válido.",
        "warn_fps_title": "FPS fora do intervalo",
        "warn_fps_msg": "A taxa de quadros deve ser um número entre 1 e 60 fps.",
        "warn_vorbis_title": "Bitrate de áudio muito baixo para Vorbis",
        "warn_vorbis_msg": "libvorbis não aceita bitrates tão baixos quanto 30k (erro -22). Use pelo menos 64k ou mude o áudio para libopus.",
        "warn_same_title": "Mesmo arquivo",
        "warn_same_msg": "A entrada e a saída apontam para o mesmo arquivo. Altere o nome do arquivo.",
        "conv_prep": "Calculando duração e preparando conversão VBR...",
        "conv_prog": "Convertendo para {codec}{res}{fps} ({bitrate} VBR)... {pct:.1f}%",
        "conv_fin": "Finalizando arquivo WebM...",
        "conv_done": "Concluído: salvo em {out_file}",
        "conv_err": "O FFmpeg retornou erro:\n{err}",
        "conv_no_ff": "ffmpeg.exe não foi encontrado ao lado do script ou executável.",
        "conv_unexp": "Erro inesperado: {err}",
        "conv_unknown": "Erro desconhecido no FFmpeg.",
        "conv_done_title": "Conversão concluída",
        "conv_err_title": "Erro na conversão",
    },
}


def parse_db_value(value_str):
    """Convierte texto como '0', '3.5', '+6' o '6,5' en float, o None si es inválido."""
    raw = (value_str or "").strip().replace(",", ".")
    if not raw:
        return 0.0
    try:
        val = float(raw)
    except ValueError:
        return None
    if val < -24.0 or val > 24.0:
        return None
    return val


def vorbis_quality_from_kbps(audio_kbps):
    """Calcula calidad VBR (-q:a de 3 a 10 en libvorbis) priorizando fidelidad sonora."""
    if audio_kbps is None or audio_kbps <= 0:
        return 7
    if audio_kbps >= 320:
        return 9
    if audio_kbps >= 256:
        return 8
    if audio_kbps >= 192:
        return 7
    if audio_kbps >= 160:
        return 6
    if audio_kbps >= 128:
        return 5
    if audio_kbps >= 96:
        return 4
    return 3


def open_output_dir_fallback(output_dir):
    """Abre la carpeta Output como respaldo si no se puede abrir ningún reproductor."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        if os.name == "nt":
            os.startfile(output_dir)
        else:
            subprocess.Popen(["xdg-open", output_dir])
    except Exception:
        pass


def find_installed_player():
    """Busca reproductores instalados comunes (VLC, MPC-HC, MPV) en PATH o rutas estándar."""
    player_names = ["vlc.exe", "mpc-hc64.exe", "mpc-hc.exe", "mpv.exe"] if os.name == "nt" else ["vlc", "mpv"]
    for name in player_names:
        found = shutil.which(name)
        if found:
            return os.path.abspath(found)

    if os.name == "nt":
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pfx86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local_app = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(pf, "VideoLAN", "VLC", "vlc.exe"),
            os.path.join(pfx86, "VideoLAN", "VLC", "vlc.exe"),
            os.path.join(pf, "K-Lite Codec Pack", "MPC-HC64", "mpc-hc64.exe"),
            os.path.join(pfx86, "K-Lite Codec Pack", "MPC-HC", "mpc-hc.exe"),
            os.path.join(local_app, "Programs", "mpv", "mpv.exe"),
        ]
        for path in candidates:
            if path and os.path.isfile(path):
                return os.path.abspath(path)
    return None


def open_preview_or_output(media_path, output_dir):
    """Abre un reproductor instalado o nativo; si no se puede abrir, abre la carpeta Output."""
    if not media_path or not os.path.isfile(media_path):
        open_output_dir_fallback(output_dir)
        return

    player_exe = find_installed_player()
    try:
        if player_exe:
            subprocess.Popen([player_exe, media_path])
            return
    except Exception:
        pass

    try:
        if os.name == "nt":
            os.startfile(media_path)
            return
        subprocess.Popen(["xdg-open", media_path])
        return
    except Exception:
        pass

    open_output_dir_fallback(output_dir)


def get_app_dir():
    """Devuelve la carpeta donde está el .exe (si está compilado) o el .pyw."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def fetch_ffmpeg_zip_url_from_official_page():
    """Consulta ffmpeg.org/download.html y busca un enlace .zip de compilación para Windows."""
    req = urllib.request.Request(
        FFMPEG_OFFICIAL_PAGE,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
    zip_candidates = []
    for raw_href in hrefs:
        full_url = urllib.parse.urljoin(FFMPEG_OFFICIAL_PAGE, raw_href)
        lower_url = full_url.lower()
        if lower_url.endswith(".zip") and ("ffmpeg" in lower_url or "win" in lower_url):
            zip_candidates.append(full_url)

    for url in zip_candidates:
        if "essentials" in url.lower() or "release" in url.lower() or "win64" in url.lower():
            return url

    if zip_candidates:
        return zip_candidates[0]

    return FFMPEG_FALLBACK_ZIP_URL


def scan_local_for_tool(exe_name):
    """Busca primero junto al programa, luego en PATH y en carpetas comunes de usuario."""
    local_path = os.path.join(get_app_dir(), exe_name)
    if os.path.isfile(local_path):
        return os.path.abspath(local_path)

    cmd_name = exe_name.replace(".exe", "") if os.name != "nt" else exe_name
    which_path = shutil.which(cmd_name) or shutil.which(exe_name)
    if which_path:
        return os.path.abspath(which_path)

    candidate_roots = [
        r"C:\ffmpeg",
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "ffmpeg"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "ffmpeg"),
        os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"),
        os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
    ]

    target_lower = exe_name.lower()
    for root_dir in candidate_roots:
        if not root_dir or not os.path.isdir(root_dir):
            continue
        for current_root, _dirs, files in os.walk(root_dir):
            depth = current_root.replace(root_dir, "").count(os.sep)
            if depth > 4:
                continue
            for fname in files:
                if fname.lower() == target_lower:
                    return os.path.abspath(os.path.join(current_root, fname))

    return None


def normalize_kbps(value_str, default_kbps="15000k"):
    raw = (value_str or "").strip()
    if not raw:
        return default_kbps
    if re.fullmatch(r"\d+(\.\d+)?", raw):
        return f"{raw}k"
    return raw


def parse_bitrate_kbps_number(value_str):
    raw = (value_str or "").strip().lower().replace(",", ".")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(k|m)?", raw)
    if not match:
        return None
    num = float(match.group(1))
    unit = match.group(2) or "k"
    return num * 1000.0 if unit == "m" else num


def parse_fps_1_to_60(value_str):
    """Valida y devuelve un FPS entre 1 y 60, o None si no es válido."""
    raw = (value_str or "").strip().replace(",", ".")
    if not raw:
        return None
    try:
        val = float(raw)
    except ValueError:
        return None
    if val < 1.0 or val > 60.0:
        return None
    if val.is_integer():
        return str(int(val))
    return f"{val:g}"


def get_unique_output_path(desired_path):
    """Devuelve desired_path si no existe, o '<base> 1<ext>', '<base> 2<ext>', etc."""
    if not os.path.exists(desired_path):
        return desired_path

    folder = os.path.dirname(desired_path)
    filename = os.path.basename(desired_path)
    base, ext = os.path.splitext(filename)

    counter = 1
    while True:
        candidate = os.path.join(folder, f"{base} {counter}{ext}")
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def get_duration_seconds(ffprobe_cmd, input_file, creationflags):
    if not ffprobe_cmd:
        return None
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file,
    ]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creationflags,
        )
        if proc.returncode == 0:
            val = float(proc.stdout.strip())
            if val > 0:
                return val
    except Exception:
        pass
    return None


def get_video_height(ffprobe_cmd, input_file, creationflags):
    if not ffprobe_cmd:
        return None
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=height",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file,
    ]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creationflags,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return int(float(proc.stdout.strip()))
    except Exception:
        pass
    return None


def build_detail_scale_filter(target_height, source_height=None):
    """Escala a target_height con alta precisión y añade detalle suave si sube de resolución."""
    h = int(target_height)
    scale_part = f"scale=-2:{h}:flags=lanczos+accurate_rnd+full_chroma_int"
    if source_height is not None and source_height < h:
        return f"{scale_part},unsharp=3:3:0.35:3:3:0.0"
    return scale_part


class WebMConverterApp:
    def __init__(self, root):
        self.root = root
        self.lang = "es"
        self.root.title(self.tr("window_title"))
        self.root.geometry("645x865")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_dir = os.path.join(get_app_dir(), "Output")
        self.output_name_var = tk.StringVar()

        self.codec_var = tk.StringVar(value="VP8")
        self.bitrate_kbps_var = tk.StringVar(value="15000")
        self.maxrate_var = tk.StringVar(value="22000k")
        self.bufsize_var = tk.StringVar(value="30000k")
        self.crf_var = tk.StringVar(value="4")
        self.high_fidelity_var = tk.BooleanVar(value=True)

        self.resize_enabled_var = tk.BooleanVar(value=False)
        self.resolution_var = tk.StringVar(value="720p")
        self.res_note_var = tk.StringVar()

        self.fps_enabled_var = tk.BooleanVar(value=False)
        self.fps_value_var = tk.StringVar(value="60")
        self.fps_note_var = tk.StringVar()

        self.audio_codec_var = tk.StringVar(value="libopus")
        self.audio_bitrate_var = tk.StringVar(value="192k")
        self.sync_audio_path = tk.StringVar(value="")
        self.sync_audio_note_var = tk.StringVar()

        self.show_audio_section_var = tk.BooleanVar(value=True)
        self.audio_input_path = tk.StringVar()
        self.audio_output_name_var = tk.StringVar()
        self.audio_target_fmt_var = tk.StringVar(value="OGG")
        self.audio_conv_bitrate_var = tk.StringVar(value="256k")
        self.audio_gain_db_var = tk.StringVar(value="0.0")
        self.audio_limiter_var = tk.BooleanVar(value=True)
        self._preview_proc = None
        self._preview_playing = False

        self.percent_var = tk.StringVar(value="0.0%")
        self.status_var = tk.StringVar()

        self._lang_menu = tk.Menu(self.root, tearoff=0)
        self._build_ui()
        self.apply_language("es")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_window)
        self.root.after(150, self.check_ffmpeg_on_startup)

    def _on_close_window(self):
        self.stop_audio_preview(update_status=False)
        self.root.destroy()

    def tr(self, key, **kwargs):
        text = TRANSLATIONS.get(self.lang, TRANSLATIONS["es"]).get(key, TRANSLATIONS["es"].get(key, key))
        if kwargs:
            return text.format(**kwargs)
        return text

    def _rebuild_lang_menu(self):
        self._lang_menu.delete(0, "end")
        self._lang_menu.add_command(label=self.tr("lang_es"), command=lambda: self.apply_language("es"))
        self._lang_menu.add_command(label=self.tr("lang_en"), command=lambda: self.apply_language("en"))
        self._lang_menu.add_command(label=self.tr("lang_pt"), command=lambda: self.apply_language("pt"))

    def _open_lang_menu(self):
        self._rebuild_lang_menu()
        x = self.btn_lang.winfo_rootx()
        y = self.btn_lang.winfo_rooty() + self.btn_lang.winfo_height()
        self._lang_menu.tk_popup(x, y)

    def _refresh_sync_audio_note(self):
        custom_audio = (self.sync_audio_path.get() or "").strip()
        if custom_audio:
            self.sync_audio_note_var.set(self.tr("sync_audio_set", name=os.path.basename(custom_audio)))
        else:
            self.sync_audio_note_var.set(self.tr("sync_audio_none"))

    def select_synced_audio(self):
        proceed = messagebox.askyesno(
            self.tr("sync_audio_notice_title"),
            self.tr("sync_audio_notice_msg"),
        )
        if not proceed:
            return

        initial_dir = os.path.dirname(self.input_path.get().strip()) if self.input_path.get().strip() else get_app_dir()
        path = filedialog.askopenfilename(
            title=self.tr("sync_audio_dialog_title"),
            initialdir=initial_dir,
            filetypes=[
                (
                    self.tr("sync_audio_filter_media"),
                    "*.mp3 *.wav *.ogg *.opus *.m4a *.aac *.flac *.mp4 *.mkv *.mov *.avi *.webm",
                ),
                (self.tr("sync_audio_filter_audio"), "*.mp3 *.wav *.ogg *.opus *.m4a *.aac *.flac"),
                (self.tr("sync_audio_filter_video"), "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv *.ts *.m4v"),
                (self.tr("sync_audio_filter_all"), "*.*"),
            ],
        )
        if path:
            self.sync_audio_path.set(path)
            self._refresh_sync_audio_note()

    def _refresh_preview_button_text(self):
        if self._preview_playing:
            self.btn_aud_play.config(text=self.tr("btn_aud_stop"))
        else:
            self.btn_aud_play.config(text=self.tr("btn_aud_play"))

    def toggle_audio_section_visibility(self):
        if self.show_audio_section_var.get():
            self.aud_sep.pack(fill="x", padx=12, pady=4, before=self.frm_act)
            self.frm_aud_conv.pack(fill="x", padx=12, pady=4, before=self.frm_act)
            self.root.geometry("645x865")
        else:
            self.stop_audio_preview(update_status=False)
            self.frm_aud_conv.pack_forget()
            self.aud_sep.pack_forget()
            self.root.geometry("645x655")

    def apply_language(self, lang_code):
        if lang_code not in TRANSLATIONS:
            return
        self.lang = lang_code
        self.root.title(self.tr("window_title"))
        self.btn_lang.config(text=self.tr("lang_button"))
        self.chk_show_audio_sec.config(text=self.tr("chk_show_audio_sec"))
        self.frm_in.config(text=self.tr("frm_in"))
        self.btn_add.config(text=self.tr("btn_add"))
        self.frm_out.config(text=self.tr("frm_out"))
        self.lbl_name.config(text=self.tr("lbl_name"))
        self.btn_open_out.config(text=self.tr("btn_open_out"))
        self.frm_cfg.config(text=self.tr("frm_cfg"))
        self.lbl_codec.config(text=self.tr("lbl_codec"))
        self.lbl_bitrate.config(text=self.tr("lbl_bitrate"))
        self.lbl_maxrate.config(text=self.tr("lbl_maxrate"))
        self.lbl_bufsize.config(text=self.tr("lbl_bufsize"))
        self.lbl_crf.config(text=self.tr("lbl_crf"))
        self.chk_fidelity.config(text=self.tr("chk_fidelity"))
        self.chk_resize.config(text=self.tr("chk_resize"))
        self.chk_fps.config(text=self.tr("chk_fps"))
        self.lbl_audio.config(text=self.tr("lbl_audio"))
        self.lbl_abitrate.config(text=self.tr("lbl_abitrate"))
        self.btn_sync_audio.config(text=self.tr("btn_sync_audio"))
        self.btn_convert.config(text=self.tr("btn_convert"))

        self.frm_aud_conv.config(text=self.tr("frm_aud_conv"))
        self.lbl_aud_in.config(text=self.tr("lbl_aud_in"))
        self.btn_aud_add.config(text=self.tr("btn_aud_add"))
        self._refresh_preview_button_text()
        self.lbl_aud_out.config(text=self.tr("lbl_aud_out"))
        self.lbl_aud_fmt.config(text=self.tr("lbl_aud_fmt"))
        self.lbl_aud_br.config(text=self.tr("lbl_aud_br"))
        self.lbl_aud_db.config(text=self.tr("lbl_aud_db"))
        self.chk_aud_limiter.config(text=self.tr("chk_aud_limiter"))
        self.btn_aud_convert.config(text=self.tr("btn_aud_convert"))

        self._refresh_sync_audio_note()
        self._toggle_resolution_combo()
        self._toggle_fps_entry()
        if not self.status_var.get():
            self.status_var.set(self.tr("status_ready", out_dir=self.output_dir))

    def _ask_install_ffmpeg_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(self.tr("dlg_no_ffmpeg_title"))
        dlg.geometry("430x165")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        choice = {"install": False}

        frm = ttk.Frame(dlg, padding=16)
        frm.pack(fill="both", expand=True)

        ttk.Label(
            frm,
            text=self.tr("dlg_no_ffmpeg_msg"),
            wraplength=390,
        ).pack(anchor="w", pady=(0, 14))

        btns = ttk.Frame(frm)
        btns.pack(fill="x")

        def on_install():
            choice["install"] = True
            dlg.destroy()

        def on_cancel():
            choice["install"] = False
            dlg.destroy()

        ttk.Button(btns, text=self.tr("btn_install"), command=on_install).pack(side="right", padx=(8, 0))
        ttk.Button(btns, text=self.tr("btn_cancel"), command=on_cancel).pack(side="right")

        dlg.protocol("WM_DELETE_WINDOW", on_cancel)
        self.root.wait_window(dlg)
        return choice["install"]

    def check_ffmpeg_on_startup(self):
        ffmpeg_cmd = scan_local_for_tool("ffmpeg.exe")
        ffprobe_cmd = scan_local_for_tool("ffprobe.exe")

        if ffmpeg_cmd and ffprobe_cmd:
            self.status_var.set(self.tr("status_detected"))
            return

        if self._ask_install_ffmpeg_dialog():
            self._start_ffmpeg_install()
        else:
            self.status_var.set(self.tr("status_no_ffmpeg"))

    def _start_ffmpeg_install(self):
        self.stop_audio_preview(update_status=False)
        self.btn_convert.config(state="disabled")
        self.btn_aud_convert.config(state="disabled")
        self.progress["value"] = 5.0
        self.percent_var.set("5.0%")
        self.status_var.set(self.tr("inst_start"))

        threading.Thread(target=self._install_ffmpeg_worker, daemon=True).start()

    def _download_with_progress(self, url, dest_path):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp, open(dest_path, "wb") as out:
            total = resp.headers.get("Content-Length")
            total_bytes = int(total) if total and total.isdigit() else 0
            downloaded = 0
            chunk_size = 65536
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                out.write(chunk)
                downloaded += len(chunk)
                mb_done = downloaded / (1024 * 1024)
                if total_bytes > 0:
                    ratio = min(1.0, downloaded / total_bytes)
                    pct = 15.0 + ratio * 60.0
                else:
                    pct = min(74.0, 15.0 + (mb_done / 90.0) * 59.0)
                self.root.after(
                    0,
                    self._update_progress,
                    pct,
                    self.tr("inst_dl", mb=mb_done, pct=pct),
                )

    def _install_ffmpeg_worker(self):
        app_dir = get_app_dir()
        tmp_zip = os.path.join(tempfile.gettempdir(), "ffmpeg_official_download.zip")
        try:
            self.root.after(0, self._update_progress, 10.0, self.tr("inst_page"))
            try:
                download_url = fetch_ffmpeg_zip_url_from_official_page()
            except Exception:
                download_url = FFMPEG_FALLBACK_ZIP_URL

            self.root.after(0, self._update_progress, 15.0, self.tr("inst_connect"))
            try:
                self._download_with_progress(download_url, tmp_zip)
            except Exception:
                if download_url != FFMPEG_FALLBACK_ZIP_URL:
                    self._download_with_progress(FFMPEG_FALLBACK_ZIP_URL, tmp_zip)
                else:
                    raise

            self.root.after(0, self._update_progress, 76.0, self.tr("inst_extract_start"))
            extracted = set()
            target_bins = ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe")
            with zipfile.ZipFile(tmp_zip, "r") as zf:
                matching = [m for m in zf.namelist() if os.path.basename(m).lower() in target_bins]
                total_bins = max(1, len(matching))
                for idx, member in enumerate(matching, start=1):
                    base_name = os.path.basename(member)
                    dest_path = os.path.join(app_dir, base_name)
                    with zf.open(member) as src, open(dest_path, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    extracted.add(base_name.lower())
                    pct = 76.0 + (idx / total_bins) * 22.0
                    self.root.after(
                        0,
                        self._update_progress,
                        pct,
                        self.tr("inst_extract_file", name=base_name, pct=pct),
                    )

            if "ffmpeg.exe" in extracted and "ffprobe.exe" in extracted:
                self.root.after(
                    0,
                    self._finish_ffmpeg_install,
                    True,
                    self.tr("inst_done", app_dir=app_dir),
                )
            else:
                self.root.after(
                    0,
                    self._finish_ffmpeg_install,
                    False,
                    self.tr("inst_missing_bins"),
                )
        except Exception as exc:
            self.root.after(
                0,
                self._finish_ffmpeg_install,
                False,
                self.tr("inst_err", err=exc),
            )
        finally:
            if os.path.isfile(tmp_zip):
                try:
                    os.remove(tmp_zip)
                except Exception:
                    pass

    def _finish_ffmpeg_install(self, ok, msg):
        self.btn_convert.config(state="normal")
        self.btn_aud_convert.config(state="normal")
        if ok:
            self.progress["value"] = 100.0
            self.percent_var.set("100.0%")
            self.status_var.set(msg)
            messagebox.showinfo(self.tr("inst_done_title"), msg)
        else:
            self.progress["value"] = 0.0
            self.percent_var.set("0.0%")
            self.status_var.set(msg)
            messagebox.showerror(self.tr("inst_err_title"), msg)

    def _build_output_filepath(self):
        raw_name = (self.output_name_var.get() or "").strip()
        if not raw_name:
            in_file = self.input_path.get().strip()
            raw_name = os.path.splitext(os.path.basename(in_file))[0] if in_file else "salida"

        base, ext = os.path.splitext(raw_name)
        if ext.lower() != ".webm":
            file_name = f"{raw_name}.webm"
        else:
            file_name = f"{base}.webm"

        desired = os.path.join(self.output_dir, file_name)
        return desired, get_unique_output_path(desired)

    def _build_audio_output_filepath(self):
        fmt_upper = (self.audio_target_fmt_var.get() or "OGG").upper()
        if fmt_upper == "OPUS":
            target_ext = ".opus"
        elif fmt_upper == "WAV":
            target_ext = ".wav"
        else:
            target_ext = ".ogg"

        raw_name = (self.audio_output_name_var.get() or "").strip()
        if not raw_name:
            in_aud = self.audio_input_path.get().strip()
            raw_name = os.path.splitext(os.path.basename(in_aud))[0] if in_aud else "audio_salida"

        base, ext = os.path.splitext(raw_name)
        if ext.lower() != target_ext:
            file_name = f"{raw_name}{target_ext}"
        else:
            file_name = f"{base}{target_ext}"

        desired = os.path.join(self.output_dir, file_name)
        return desired, get_unique_output_path(desired)

    def _build_ui(self):
        pad = {"padx": 12, "pady": 4}

        frm_top = ttk.Frame(self.root)
        frm_top.pack(fill="x", padx=12, pady=(6, 2))
        self.chk_show_audio_sec = ttk.Checkbutton(
            frm_top,
            text="",
            variable=self.show_audio_section_var,
            command=self.toggle_audio_section_visibility,
        )
        self.chk_show_audio_sec.pack(side="left")
        self.btn_lang = ttk.Button(frm_top, text="Language", command=self._open_lang_menu, width=12)
        self.btn_lang.pack(side="right")

        self.frm_in = ttk.LabelFrame(self.root, text="")
        self.frm_in.pack(fill="x", **pad)
        ttk.Entry(self.frm_in, textvariable=self.input_path, width=60).pack(side="left", padx=(8, 6), pady=6)
        self.btn_add = ttk.Button(self.frm_in, text="", command=self.select_input)
        self.btn_add.pack(side="left", padx=(0, 8), pady=6)

        self.frm_out = ttk.LabelFrame(self.root, text="")
        self.frm_out.pack(fill="x", **pad)

        row_file = ttk.Frame(self.frm_out)
        row_file.pack(fill="x", padx=8, pady=6)
        self.lbl_name = ttk.Label(row_file, text="", width=15)
        self.lbl_name.pack(side="left")
        ttk.Entry(row_file, textvariable=self.output_name_var, width=42).pack(side="left", padx=(0, 6))
        self.btn_open_out = ttk.Button(row_file, text="", command=self.open_output_folder)
        self.btn_open_out.pack(side="left")

        self.frm_cfg = ttk.LabelFrame(self.root, text="")
        self.frm_cfg.pack(fill="x", **pad)

        grid_opts = {"padx": 8, "pady": 4, "sticky": "w"}

        self.lbl_codec = ttk.Label(self.frm_cfg, text="")
        self.lbl_codec.grid(row=0, column=0, **grid_opts)
        cb_codec = ttk.Combobox(
            self.frm_cfg,
            textvariable=self.codec_var,
            values=["VP8", "VP9"],
            state="readonly",
            width=10,
        )
        cb_codec.grid(row=0, column=1, **grid_opts)

        self.lbl_bitrate = ttk.Label(self.frm_cfg, text="")
        self.lbl_bitrate.grid(row=0, column=2, **grid_opts)
        ttk.Entry(self.frm_cfg, textvariable=self.bitrate_kbps_var, width=12).grid(row=0, column=3, **grid_opts)

        self.lbl_maxrate = ttk.Label(self.frm_cfg, text="")
        self.lbl_maxrate.grid(row=1, column=0, **grid_opts)
        ttk.Entry(self.frm_cfg, textvariable=self.maxrate_var, width=12).grid(row=1, column=1, **grid_opts)

        self.lbl_bufsize = ttk.Label(self.frm_cfg, text="")
        self.lbl_bufsize.grid(row=1, column=2, **grid_opts)
        ttk.Entry(self.frm_cfg, textvariable=self.bufsize_var, width=12).grid(row=1, column=3, **grid_opts)

        self.lbl_crf = ttk.Label(self.frm_cfg, text="")
        self.lbl_crf.grid(row=2, column=0, **grid_opts)
        ttk.Entry(self.frm_cfg, textvariable=self.crf_var, width=12).grid(row=2, column=1, **grid_opts)

        self.chk_fidelity = ttk.Checkbutton(
            self.frm_cfg,
            text="",
            variable=self.high_fidelity_var,
        )
        self.chk_fidelity.grid(row=2, column=2, columnspan=2, **grid_opts)

        self.chk_resize = ttk.Checkbutton(
            self.frm_cfg,
            text="",
            variable=self.resize_enabled_var,
            command=self._toggle_resolution_combo,
        )
        self.chk_resize.grid(row=3, column=0, columnspan=2, **grid_opts)

        self.cb_res = ttk.Combobox(
            self.frm_cfg,
            textvariable=self.resolution_var,
            values=["240p", "360p", "480p", "540p", "720p", "1080p"],
            state="disabled",
            width=9,
        )
        self.cb_res.grid(row=3, column=2, **grid_opts)
        self.cb_res.bind("<<ComboboxSelected>>", lambda _e: self._toggle_resolution_combo())

        ttk.Label(self.frm_cfg, textvariable=self.res_note_var).grid(row=3, column=3, **grid_opts)

        self.chk_fps = ttk.Checkbutton(
            self.frm_cfg,
            text="",
            variable=self.fps_enabled_var,
            command=self._toggle_fps_entry,
        )
        self.chk_fps.grid(row=4, column=0, columnspan=2, **grid_opts)

        self.ent_fps = ttk.Entry(
            self.frm_cfg,
            textvariable=self.fps_value_var,
            state="disabled",
            width=10,
        )
        self.ent_fps.grid(row=4, column=2, **grid_opts)
        self.ent_fps.bind("<KeyRelease>", lambda _e: self._toggle_fps_entry())

        ttk.Label(self.frm_cfg, textvariable=self.fps_note_var).grid(row=4, column=3, **grid_opts)

        self.lbl_audio = ttk.Label(self.frm_cfg, text="")
        self.lbl_audio.grid(row=5, column=0, **grid_opts)
        cb_audio = ttk.Combobox(
            self.frm_cfg,
            textvariable=self.audio_codec_var,
            values=["libopus", "libvorbis", "none"],
            state="readonly",
            width=10,
        )
        cb_audio.grid(row=5, column=1, **grid_opts)

        self.lbl_abitrate = ttk.Label(self.frm_cfg, text="")
        self.lbl_abitrate.grid(row=5, column=2, **grid_opts)
        ttk.Entry(self.frm_cfg, textvariable=self.audio_bitrate_var, width=12).grid(row=5, column=3, **grid_opts)

        self.btn_sync_audio = ttk.Button(self.frm_cfg, text="", command=self.select_synced_audio)
        self.btn_sync_audio.grid(row=6, column=0, columnspan=2, **grid_opts)
        ttk.Label(self.frm_cfg, textvariable=self.sync_audio_note_var).grid(row=6, column=2, columnspan=2, **grid_opts)

        row_vid_btn = ttk.Frame(self.root)
        row_vid_btn.pack(fill="x", padx=12, pady=(2, 4))
        self.btn_convert = ttk.Button(row_vid_btn, text="", command=self.start_conversion, width=22)
        self.btn_convert.pack(side="left")

        self.aud_sep = ttk.Separator(self.root, orient="horizontal")
        self.aud_sep.pack(fill="x", padx=12, pady=4)

        self.frm_aud_conv = ttk.LabelFrame(self.root, text="")
        self.frm_aud_conv.pack(fill="x", **pad)

        row_aud_in = ttk.Frame(self.frm_aud_conv)
        row_aud_in.pack(fill="x", padx=8, pady=(6, 4))
        self.lbl_aud_in = ttk.Label(row_aud_in, text="", width=16)
        self.lbl_aud_in.pack(side="left")
        ttk.Entry(row_aud_in, textvariable=self.audio_input_path, width=29).pack(side="left", padx=(0, 6))
        self.btn_aud_add = ttk.Button(row_aud_in, text="", command=self.select_audio_input, width=16)
        self.btn_aud_add.pack(side="left", padx=(0, 6))
        self.btn_aud_play = ttk.Button(row_aud_in, text="", command=self.toggle_audio_preview, width=11)
        self.btn_aud_play.pack(side="left")

        row_aud_out = ttk.Frame(self.frm_aud_conv)
        row_aud_out.pack(fill="x", padx=8, pady=(2, 4))
        self.lbl_aud_out = ttk.Label(row_aud_out, text="", width=16)
        self.lbl_aud_out.pack(side="left")
        ttk.Entry(row_aud_out, textvariable=self.audio_output_name_var, width=22).pack(side="left", padx=(0, 8))

        self.lbl_aud_fmt = ttk.Label(row_aud_out, text="")
        self.lbl_aud_fmt.pack(side="left", padx=(0, 4))
        cb_aud_fmt = ttk.Combobox(
            row_aud_out,
            textvariable=self.audio_target_fmt_var,
            values=["OGG", "OPUS", "WAV"],
            state="readonly",
            width=7,
        )
        cb_aud_fmt.pack(side="left", padx=(0, 8))

        self.lbl_aud_br = ttk.Label(row_aud_out, text="")
        self.lbl_aud_br.pack(side="left", padx=(0, 4))
        ttk.Entry(row_aud_out, textvariable=self.audio_conv_bitrate_var, width=8).pack(side="left")

        row_aud_db = ttk.Frame(self.frm_aud_conv)
        row_aud_db.pack(fill="x", padx=8, pady=(2, 4))
        self.lbl_aud_db = ttk.Label(row_aud_db, text="", width=16)
        self.lbl_aud_db.pack(side="left")
        ent_db = ttk.Entry(row_aud_db, textvariable=self.audio_gain_db_var, width=8)
        ent_db.pack(side="left", padx=(0, 6))
        ent_db.bind("<KeyRelease>", lambda _e: self._restart_preview_if_playing())
        ttk.Scale(
            row_aud_db,
            from_=0.0,
            to=12.0,
            orient="horizontal",
            length=150,
            command=self._on_db_slider_change,
        ).pack(side="left", padx=(0, 10))
        self.chk_aud_limiter = ttk.Checkbutton(
            row_aud_db,
            text="",
            variable=self.audio_limiter_var,
            command=self._restart_preview_if_playing,
        )
        self.chk_aud_limiter.pack(side="left")

        row_aud_act = ttk.Frame(self.frm_aud_conv)
        row_aud_act.pack(fill="x", padx=8, pady=(4, 6))
        self.btn_aud_convert = ttk.Button(row_aud_act, text="", command=self.start_audio_conversion, width=22)
        self.btn_aud_convert.pack(side="left")

        self.frm_act = ttk.Frame(self.root)
        self.frm_act.pack(fill="x", **pad)

        self.progress = ttk.Progressbar(self.frm_act, mode="determinate", maximum=100, length=520)
        self.progress.pack(side="left", fill="x", expand=True)

        ttk.Label(self.root, textvariable=self.percent_var, width=7, anchor="e").pack(side="left", padx=(8, 4))

        ttk.Label(self.root, textvariable=self.status_var, wraplength=615).pack(fill="x", padx=12, pady=(4, 8))

    def _on_db_slider_change(self, val_str):
        try:
            val = float(val_str)
            self.audio_gain_db_var.set(f"{val:.1f}")
            self._restart_preview_if_playing()
        except ValueError:
            pass

    def _build_audio_filter_chain(self, gain_db, use_limiter):
        af_filters = []
        if abs(gain_db) > 0.001:
            af_filters.append(f"volume={gain_db:g}dB")
        if use_limiter and gain_db > 0.001:
            af_filters.append("alimiter=limit=0.95:level=disabled")
        return ",".join(af_filters)

    def stop_audio_preview(self, update_status=True):
        proc = self._preview_proc
        self._preview_proc = None
        self._preview_playing = False
        self._refresh_preview_button_text()
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=1.5)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        if update_status:
            self.status_var.set(self.tr("aud_preview_stopped"))

    def _restart_preview_if_playing(self):
        if self._preview_playing:
            self._start_internal_audio_preview(restart=True)

    def toggle_audio_preview(self):
        if self._preview_playing:
            self.stop_audio_preview(update_status=True)
            return
        self._start_internal_audio_preview(restart=False)

    def _start_internal_audio_preview(self, restart=False):
        in_aud = self.audio_input_path.get().strip()
        if not in_aud or not os.path.isfile(in_aud):
            self.stop_audio_preview(update_status=False)
            if not restart:
                messagebox.showwarning(self.tr("aud_warn_no_file_title"), self.tr("aud_warn_no_file_msg"))
            return

        gain_db = parse_db_value(self.audio_gain_db_var.get())
        if gain_db is None:
            if not restart:
                messagebox.showwarning(self.tr("aud_warn_db_title"), self.tr("aud_warn_db_msg"))
            return

        ffplay_cmd = scan_local_for_tool("ffplay.exe")
        if not ffplay_cmd:
            self.stop_audio_preview(update_status=False)
            if not restart:
                messagebox.showwarning(self.tr("aud_no_ffplay_title"), self.tr("aud_no_ffplay_msg"))
            return

        self.stop_audio_preview(update_status=False)

        af_chain = self._build_audio_filter_chain(gain_db, bool(self.audio_limiter_var.get()))
        cmd = [
            ffplay_cmd,
            "-nodisp",
            "-autoexit",
            "-loglevel", "quiet",
            "-i", in_aud,
        ]
        if af_chain:
            cmd.extend(["-af", af_chain])

        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags,
            )
        except Exception as exc:
            messagebox.showerror(self.tr("conv_err_title"), self.tr("conv_unexp", err=exc))
            return

        self._preview_proc = proc
        self._preview_playing = True
        self._refresh_preview_button_text()

        db_tag = f"{gain_db:+.1f} dB" if abs(gain_db) > 0.001 else "0.0 dB"
        self.status_var.set(self.tr("aud_preview_playing", db_tag=db_tag))

        def _watch_preview(target_proc):
            target_proc.wait()
            self.root.after(0, self._on_preview_finished, target_proc)

        threading.Thread(target=_watch_preview, args=(proc,), daemon=True).start()

    def _on_preview_finished(self, target_proc):
        if self._preview_proc is target_proc:
            self._preview_proc = None
            self._preview_playing = False
            self._refresh_preview_button_text()
            self.status_var.set(self.tr("aud_preview_stopped"))

    def select_audio_input(self):
        path = filedialog.askopenfilename(
            title=self.tr("aud_dialog_title"),
            filetypes=[
                (
                    self.tr("sync_audio_filter_media"),
                    "*.mp3 *.wav *.ogg *.opus *.m4a *.aac *.flac *.wma *.mp4 *.mkv *.mov *.avi *.webm",
                ),
                (self.tr("sync_audio_filter_audio"), "*.mp3 *.wav *.ogg *.opus *.m4a *.aac *.flac *.wma"),
                (self.tr("sync_audio_filter_video"), "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv *.ts *.m4v"),
                (self.tr("sync_audio_filter_all"), "*.*"),
            ],
        )
        if path:
            self.stop_audio_preview(update_status=False)
            self.audio_input_path.set(path)
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.audio_output_name_var.set(base_name)
            desired_out, final_out = self._build_audio_output_filepath()
            self.percent_var.set("0.0%")
            self.progress["value"] = 0
            if final_out != desired_out:
                self.status_var.set(
                    self.tr(
                        "dup_found",
                        name=os.path.basename(desired_out),
                        final=os.path.basename(final_out),
                    )
                )
            else:
                self.status_var.set(self.tr("ready_save", final=final_out))

    def start_audio_conversion(self):
        self.stop_audio_preview(update_status=False)
        in_aud = self.audio_input_path.get().strip()
        if not in_aud or not os.path.isfile(in_aud):
            messagebox.showwarning(self.tr("aud_warn_no_file_title"), self.tr("aud_warn_no_file_msg"))
            return

        gain_db = parse_db_value(self.audio_gain_db_var.get())
        if gain_db is None:
            messagebox.showwarning(self.tr("aud_warn_db_title"), self.tr("aud_warn_db_msg"))
            return

        ffmpeg_cmd = scan_local_for_tool("ffmpeg.exe")
        if not ffmpeg_cmd:
            if self._ask_install_ffmpeg_dialog():
                self._start_ffmpeg_install()
            return

        ffprobe_cmd = scan_local_for_tool("ffprobe.exe")
        fmt_upper = (self.audio_target_fmt_var.get() or "OGG").upper()
        if fmt_upper == "OPUS":
            acodec = "libopus"
        elif fmt_upper == "WAV":
            acodec = "pcm_s16le"
        else:
            acodec = "libvorbis"

        abitrate = normalize_kbps(self.audio_conv_bitrate_var.get(), "256k")

        audio_kbps = parse_bitrate_kbps_number(abitrate)
        if acodec == "libvorbis" and audio_kbps is not None and audio_kbps < 48:
            messagebox.showwarning(self.tr("warn_vorbis_title"), self.tr("warn_vorbis_msg"))
            return

        os.makedirs(self.output_dir, exist_ok=True)
        _, out_aud_file = self._build_audio_output_filepath()
        self.audio_output_name_var.set(os.path.splitext(os.path.basename(out_aud_file))[0])

        if os.path.abspath(in_aud).lower() == os.path.abspath(out_aud_file).lower():
            messagebox.showwarning(self.tr("warn_same_title"), self.tr("warn_same_msg"))
            return

        self.btn_convert.config(state="disabled")
        self.btn_aud_convert.config(state="disabled")
        self.progress["value"] = 0
        self.percent_var.set("0.0%")
        self.status_var.set(self.tr("aud_conv_prep"))

        threading.Thread(
            target=self._run_audio_ffmpeg,
            args=(
                ffmpeg_cmd,
                ffprobe_cmd,
                in_aud,
                out_aud_file,
                fmt_upper,
                acodec,
                abitrate,
                gain_db,
                bool(self.audio_limiter_var.get()),
            ),
            daemon=True,
        ).start()

    def _run_audio_ffmpeg(
        self,
        ffmpeg_cmd,
        ffprobe_cmd,
        in_aud,
        out_aud_file,
        fmt_upper,
        acodec,
        abitrate,
        gain_db,
        use_limiter,
    ):
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        duration = get_duration_seconds(ffprobe_cmd, in_aud, creationflags)
        audio_kbps = parse_bitrate_kbps_number(abitrate)

        af_chain = self._build_audio_filter_chain(gain_db, use_limiter)

        cmd = [
            ffmpeg_cmd,
            "-y",
            "-progress", "pipe:1",
            "-nostats",
            "-i", in_aud,
            "-vn",
        ]
        if af_chain:
            cmd.extend(["-af", af_chain])

        cmd.extend(["-c:a", acodec])

        if acodec == "libvorbis":
            q_val = vorbis_quality_from_kbps(audio_kbps)
            cmd.extend(["-q:a", str(q_val)])
            br_label = f"VBR q={q_val}"
        elif acodec == "libopus":
            target_opus_kbps = max(128.0, audio_kbps) if audio_kbps is not None else 256.0
            opus_br = f"{int(round(target_opus_kbps))}k"
            cmd.extend([
                "-ar", "48000",
                "-b:a", opus_br,
                "-vbr", "on",
                "-compression_level", "10",
                "-application", "audio",
            ])
            br_label = f"{opus_br} VBR"
        else:
            br_label = "PCM 16-bit"

        db_tag = f", {gain_db:+.1f} dB" if abs(gain_db) > 0.001 else ""
        cmd.append(out_aud_file)

        stderr_lines = []
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=creationflags,
            )

            def read_stderr():
                if proc.stderr:
                    for line in proc.stderr:
                        stderr_lines.append(line.rstrip())

            err_thread = threading.Thread(target=read_stderr, daemon=True)
            err_thread.start()

            if proc.stdout:
                for line in proc.stdout:
                    line = line.strip()
                    if line.startswith("out_time_ms=") and duration and duration > 0:
                        try:
                            ms_val = int(line.split("=", 1)[1])
                            if ms_val >= 0:
                                pct = (ms_val / 1_000_000.0) / duration * 100.0
                                msg = self.tr(
                                    "aud_conv_prog",
                                    fmt=fmt_upper,
                                    bitrate=br_label,
                                    db_tag=db_tag,
                                    pct=min(100.0, pct),
                                )
                                self.root.after(0, self._update_progress, pct, msg)
                        except ValueError:
                            pass
                    elif line == "progress=end":
                        self.root.after(0, self._update_progress, 100.0, self.tr("aud_conv_fin"))

            proc.wait()
            err_thread.join(timeout=2)

            if proc.returncode == 0:
                self.root.after(
                    0,
                    self._on_done,
                    True,
                    self.tr("aud_conv_done", out_file=out_aud_file),
                    out_aud_file,
                )
            else:
                err_tail = "\n".join(stderr_lines[-8:]) if stderr_lines else self.tr("conv_unknown")
                self.root.after(0, self._on_done, False, self.tr("conv_err", err=err_tail))
        except FileNotFoundError:
            self.root.after(0, self._on_done, False, self.tr("conv_no_ff"))
        except Exception as exc:
            self.root.after(0, self._on_done, False, self.tr("conv_unexp", err=exc))

    def open_output_folder(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            if os.name == "nt":
                os.startfile(self.output_dir)
            else:
                subprocess.Popen(["xdg-open", self.output_dir])
            self.status_var.set(self.tr("folder_opened", out_dir=self.output_dir))
        except Exception as exc:
            messagebox.showerror(
                self.tr("folder_err_title"),
                self.tr("folder_err_msg", err=exc),
            )

    def _toggle_resolution_combo(self):
        if self.resize_enabled_var.get():
            self.cb_res.config(state="readonly")
            self.res_note_var.set(self.tr("res_on", res=self.resolution_var.get()))
        else:
            self.cb_res.config(state="disabled")
            self.res_note_var.set(self.tr("res_off"))

    def _toggle_fps_entry(self):
        if self.fps_enabled_var.get():
            self.ent_fps.config(state="normal")
            valid_fps = parse_fps_1_to_60(self.fps_value_var.get())
            if valid_fps:
                self.fps_note_var.set(self.tr("fps_on", fps=valid_fps))
            else:
                self.fps_note_var.set(self.tr("fps_prompt"))
        else:
            self.ent_fps.config(state="disabled")
            self.fps_note_var.set(self.tr("fps_off"))

    def select_input(self):
        path = filedialog.askopenfilename(
            title=self.tr("file_dialog_title"),
            filetypes=[
                (self.tr("file_filter_video"), "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.wmv *.ts *.m4v"),
                (self.tr("file_filter_all"), "*.*"),
            ],
        )
        if path:
            self.input_path.set(path)
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.output_name_var.set(base_name)
            desired_out, final_out = self._build_output_filepath()
            self.percent_var.set("0.0%")
            self.progress["value"] = 0
            if final_out != desired_out:
                self.status_var.set(
                    self.tr(
                        "dup_found",
                        name=os.path.basename(desired_out),
                        final=os.path.basename(final_out),
                    )
                )
            else:
                self.status_var.set(self.tr("ready_save", final=final_out))

    def start_conversion(self):
        self.stop_audio_preview(update_status=False)
        in_file = self.input_path.get().strip()

        if not in_file or not os.path.isfile(in_file):
            messagebox.showwarning(self.tr("warn_no_file_title"), self.tr("warn_no_file_msg"))
            return

        ffmpeg_cmd = scan_local_for_tool("ffmpeg.exe")
        if not ffmpeg_cmd:
            if self._ask_install_ffmpeg_dialog():
                self._start_ffmpeg_install()
            return

        ffprobe_cmd = scan_local_for_tool("ffprobe.exe")

        target_fps = None
        if self.fps_enabled_var.get():
            target_fps = parse_fps_1_to_60(self.fps_value_var.get())
            if target_fps is None:
                messagebox.showwarning(self.tr("warn_fps_title"), self.tr("warn_fps_msg"))
                return

        acodec = (self.audio_codec_var.get() or "libopus").strip()
        audio_kbps = parse_bitrate_kbps_number(self.audio_bitrate_var.get())
        if acodec == "libvorbis" and audio_kbps is not None and audio_kbps < 48:
            messagebox.showwarning(self.tr("warn_vorbis_title"), self.tr("warn_vorbis_msg"))
            return

        os.makedirs(self.output_dir, exist_ok=True)

        _, out_file = self._build_output_filepath()
        self.output_name_var.set(os.path.splitext(os.path.basename(out_file))[0])

        if os.path.abspath(in_file).lower() == os.path.abspath(out_file).lower():
            messagebox.showwarning(self.tr("warn_same_title"), self.tr("warn_same_msg"))
            return

        sync_audio_file = (self.sync_audio_path.get() or "").strip()
        if sync_audio_file and not os.path.isfile(sync_audio_file):
            sync_audio_file = ""

        self.btn_convert.config(state="disabled")
        self.btn_aud_convert.config(state="disabled")
        self.progress["value"] = 0
        self.percent_var.set("0.0%")
        self.status_var.set(self.tr("conv_prep"))

        thread = threading.Thread(
            target=self._run_ffmpeg,
            args=(ffmpeg_cmd, ffprobe_cmd, in_file, out_file, target_fps, sync_audio_file),
            daemon=True,
        )
        thread.start()

    def _update_progress(self, pct, msg):
        clamped = max(0.0, min(100.0, pct))
        self.progress["value"] = clamped
        self.percent_var.set(f"{clamped:.1f}%")
        self.status_var.set(msg)

    def _run_ffmpeg(self, ffmpeg_cmd, ffprobe_cmd, in_file, out_file, target_fps=None, sync_audio_file=""):
        choice = (self.codec_var.get() or "VP8").upper()
        vcodec = "libvpx-vp9" if choice == "VP9" else "libvpx"

        b_video = normalize_kbps(self.bitrate_kbps_var.get(), "15000k")
        maxrate = normalize_kbps(self.maxrate_var.get(), "22000k")
        bufsize = normalize_kbps(self.bufsize_var.get(), "30000k")

        raw_crf = (self.crf_var.get() or "4").strip()
        if self.high_fidelity_var.get():
            try:
                crf_num = int(raw_crf)
                crf = str(max(0, min(crf_num, 4)))
            except ValueError:
                crf = "0"
        else:
            crf = raw_crf

        acodec = (self.audio_codec_var.get() or "libopus").strip()
        abitrate = normalize_kbps(self.audio_bitrate_var.get(), "192k")

        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        duration = get_duration_seconds(ffprobe_cmd, in_file, creationflags)

        cmd = [
            ffmpeg_cmd,
            "-y",
            "-progress", "pipe:1",
            "-nostats",
            "-i", in_file,
        ]
        if sync_audio_file:
            cmd.extend(["-i", sync_audio_file])

        cmd.extend(["-c:v", vcodec])

        if self.resize_enabled_var.get():
            res_map = {
                "240p": 240,
                "360p": 360,
                "480p": 480,
                "540p": 540,
                "720p": 720,
                "1080p": 1080,
            }
            target_h = res_map.get(self.resolution_var.get(), 720)
            src_h = get_video_height(ffprobe_cmd, in_file, creationflags)
            cmd.extend(["-vf", build_detail_scale_filter(target_h, src_h)])

        cmd.extend([
            "-b:v", b_video,
            "-maxrate", maxrate,
            "-bufsize", bufsize,
            "-crf", crf,
            "-quality", "good",
            "-cpu-used", "2",
        ])

        if target_fps is not None:
            cmd.extend(["-r", target_fps])
        else:
            cmd.extend(["-fps_mode", "passthrough"])

        if vcodec == "libvpx-vp9":
            cmd.extend(["-row-mt", "1"])

        if acodec == "none":
            cmd.extend(["-map", "0:v:0", "-an"])
        elif sync_audio_file:
            cmd.extend(["-map", "0:v:0", "-map", "1:a:0?", "-c:a", acodec, "-b:a", abitrate])
        else:
            cmd.extend(["-c:a", acodec, "-b:a", abitrate])

        cmd.extend(["-f", "webm", out_file])

        stderr_lines = []
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=creationflags,
            )

            def read_stderr():
                if proc.stderr:
                    for line in proc.stderr:
                        stderr_lines.append(line.rstrip())

            err_thread = threading.Thread(target=read_stderr, daemon=True)
            err_thread.start()

            if proc.stdout:
                for line in proc.stdout:
                    line = line.strip()
                    if line.startswith("out_time_ms=") and duration and duration > 0:
                        try:
                            ms_val = int(line.split("=", 1)[1])
                            if ms_val >= 0:
                                pct = (ms_val / 1_000_000.0) / duration * 100.0
                                res_tag = (
                                    f" @ {self.resolution_var.get()}"
                                    if self.resize_enabled_var.get()
                                    else ""
                                )
                                fps_tag = f" {target_fps}fps" if target_fps is not None else ""
                                msg = self.tr(
                                    "conv_prog",
                                    codec=choice,
                                    res=res_tag,
                                    fps=fps_tag,
                                    bitrate=b_video,
                                    pct=min(100.0, pct),
                                )
                                self.root.after(0, self._update_progress, pct, msg)
                        except ValueError:
                            pass
                    elif line == "progress=end":
                        self.root.after(0, self._update_progress, 100.0, self.tr("conv_fin"))

            proc.wait()
            err_thread.join(timeout=2)

            if proc.returncode == 0:
                self.root.after(0, self._on_done, True, self.tr("conv_done", out_file=out_file), out_file)
            else:
                err_tail = "\n".join(stderr_lines[-8:]) if stderr_lines else self.tr("conv_unknown")
                self.root.after(0, self._on_done, False, self.tr("conv_err", err=err_tail))
        except FileNotFoundError:
            self.root.after(0, self._on_done, False, self.tr("conv_no_ff"))
        except Exception as exc:
            self.root.after(0, self._on_done, False, self.tr("conv_unexp", err=exc))

    def _on_done(self, ok, msg, out_file=""):
        self.btn_convert.config(state="normal")
        self.btn_aud_convert.config(state="normal")
        if ok:
            self.progress["value"] = 100.0
            self.percent_var.set("100.0%")
        self.status_var.set(msg)
        if ok:
            messagebox.showinfo(self.tr("conv_done_title"), msg)
            open_preview_or_output(out_file, self.output_dir)
        else:
            messagebox.showerror(self.tr("conv_err_title"), msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = WebMConverterApp(root)
    root.mainloop()