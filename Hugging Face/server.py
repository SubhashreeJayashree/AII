import io
import os
import tempfile
import subprocess
from fastapi import FastAPI, UploadFile, Form  # pyright: ignore[reportMissingImports]
from fastapi.responses import Response  # pyright: ignore[reportMissingImports]
from TTS.api import TTS  # pyright: ignore[reportMissingImports]
import torch  # pyright: ignore[reportMissingImports]
from pydub import AudioSegment  # pyright: ignore[reportMissingImports]

app = FastAPI(title="Voice Cloning API")

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(MODEL_NAME).to(device)

def to_wav_bytes(file_bytes: bytes) -> bytes:
    # Convert any input (webm/mp3/m4a) to WAV (16kHz mono) for XTTS
    audio = AudioSegment.from_file(io.BytesIO(file_bytes))
    audio = audio.set_frame_rate(16000).set_channels(1)
    out_buf = io.BytesIO()
    audio.export(out_buf, format="wav")
    return out_buf.getvalue()

@app.post("/api/clone")
async def clone(
    reference: UploadFile,
    text: str = Form(...),
    language: str = Form("en"),
    speaker_boost: float = Form(1.0),
    speed: float = Form(1.0),
    temperature: float = Form(0.7),
):
    ref_bytes = await reference.read()
    wav_bytes = to_wav_bytes(ref_bytes)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(wav_bytes)
        tmp_path = tmp.name

    try:
        wav = tts.tts(
            text=text,
            speaker_wav=tmp_path,
            language=language,
            speaker_boost=speaker_boost,
            speed=speed,
            temperature=temperature
        )
        out_buf = io.BytesIO()
        tts.save_wav(wav=wav, path=out_buf)  # save to buffer
        audio_bytes = out_buf.getvalue()
        return Response(content=audio_bytes, media_type="audio/wav")
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
