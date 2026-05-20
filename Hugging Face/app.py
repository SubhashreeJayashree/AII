import gradio as gr  # pyright: ignore[reportMissingImports]
import torch  # pyright: ignore[reportMissingImports]
import os
from TTS.api import TTS  # pyright: ignore[reportMissingImports]

# Load XTTS model once (CPU or GPU). On Spaces, GPU is optional but speeds up.
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(MODEL_NAME).to(device)

def clone_and_speak(reference_audio, text, language, speaker_boost, speed, temperature):
    if reference_audio is None or text.strip() == "":
        return None, "Please provide a short reference audio and some text."

    # Generate speech with zero-shot cloning
    try:
        wav = tts.tts(
            text=text,
            speaker_wav=reference_audio,
            language=language,
            speaker_boost=speaker_boost,
            speed=speed,
            temperature=temperature
        )
        # Save to a temp file
        out_path = "output.wav"
        tts.save_wav(wav=wav, path=out_path)
        return out_path, "Done."
    except Exception as e:
        return None, f"Error: {e}"

with gr.Blocks(title="Zero‑Shot Voice Cloning (XTTS)") as demo:
    gr.Markdown(
        """
        # Zero‑Shot Voice Cloning
        1. Record or upload ~5–10 seconds of clear speech (single speaker).
        2. Enter text and generate audio in the cloned voice.
        """
    )

    with gr.Row():
        with gr.Column():
            ref = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Reference voice (5–10s)"
            )
            txt = gr.Textbox(
                label="Text to speak",
                placeholder="Type what you want the cloned voice to say..."
            )
            lang = gr.Dropdown(
                choices=["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "ko", "hi"],
                value="en",
                label="Language"
            )
            speaker_boost = gr.Slider(0.0, 2.0, value=1.0, step=0.1, label="Speaker boost (strength)")
            speed = gr.Slider(0.5, 1.5, value=1.0, step=0.05, label="Speed")
            temperature = gr.Slider(0.1, 1.0, value=0.7, step=0.05, label="Temperature (variation)")
            btn = gr.Button("Clone & Generate")

        with gr.Column():
            out_audio = gr.Audio(type="filepath", label="Output audio")
            status = gr.Textbox(label="Status", interactive=False)

    btn.click(
        fn=clone_and_speak,
        inputs=[ref, txt, lang, speaker_boost, speed, temperature],
        outputs=[out_audio, status]
    )

if __name__ == "__main__":
    demo.launch()
