async function recordVoiceNote(onUploaded) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("Recording not supported in this browser");
    return;
  }
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  const chunks = [];
  recorder.ondataavailable = (e) => chunks.push(e.data);
  recorder.start();
  const stop = () => new Promise((resolve) => {
    recorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      const fd = new FormData();
      fd.append("audio", blob, "voice.webm");
      try {
        const res = await fetch("/api/upload-voice", { method: "POST", body: fd });
        const json = await res.json();
        if (onUploaded) onUploaded(json, blob);
        stream.getTracks().forEach(t => t.stop());
        resolve(json);
      } catch (err) {
        console.error("Upload failed", err);
        alert("Upload failed: " + err.message);
        stream.getTracks().forEach(t => t.stop());
        resolve({ error: err.message });
      }
    };
    recorder.stop();
  });
  return { stop };
}
