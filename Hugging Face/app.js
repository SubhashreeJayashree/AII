let mediaRecorder;
let recordedChunks = [];
let referenceBlob = null;

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const uploadInput = document.getElementById("uploadInput");
const referencePlayer = document.getElementById("referencePlayer");

const textInput = document.getElementById("textInput");
const languageSelect = document.getElementById("languageSelect");
const boostSlider = document.getElementById("boostSlider");
const speedSlider = document.getElementById("speedSlider");
const tempSlider = document.getElementById("tempSlider");
const boostValue = document.getElementById("boostValue");
const speedValue = document.getElementById("speedValue");
const tempValue = document.getElementById("tempValue");

const generateBtn = document.getElementById("generateBtn");
const statusEl = document.getElementById("status");
const outputPlayer = document.getElementById("outputPlayer");
const downloadLink = document.getElementById("downloadLink");

// slider readouts
boostSlider.addEventListener("input", () => (boostValue.textContent = boostSlider.value));
speedSlider.addEventListener("input", () => (speedValue.textContent = speedSlider.value));
tempSlider.addEventListener("input", () => (tempValue.textContent = tempSlider.value));

// recording
recordBtn.addEventListener("click", async () => {
  recordedChunks = [];
  statusEl.textContent = "Recording…";
  recordBtn.disabled = true;
  stopBtn.disabled = false;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data);
    };
    mediaRecorder.onstop = () => {
      referenceBlob = new Blob(recordedChunks, { type: "audio/webm" });
      referencePlayer.src = URL.createObjectURL(referenceBlob);
      statusEl.textContent = "Recorded reference sample.";
    };
    mediaRecorder.start();
  } catch (err) {
    statusEl.textContent = `Mic error: ${err.message}`;
    recordBtn.disabled = false;
    stopBtn.disabled = true;
  }
});

stopBtn.addEventListener("click", () => {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
  recordBtn.disabled = false;
  stopBtn.disabled = true;
});

// upload
uploadInput.addEventListener("change", () => {
  const file = uploadInput.files?.[0];
  if (!file) return;
  referenceBlob = file;
  referencePlayer.src = URL.createObjectURL(file);
  statusEl.textContent = "Uploaded reference sample.";
});

// generate
generateBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  if (!referenceBlob) {
    statusEl.textContent = "Please record or upload a reference sample.";
    return;
  }
  if (!text) {
    statusEl.textContent = "Please enter text to speak.";
    return;
  }

  statusEl.textContent = "Cloning and generating…";
  generateBtn.disabled = true;

  try {
    const form = new FormData();
    form.append("reference", referenceBlob, "reference.webm");
    form.append("text", text);
    form.append("language", languageSelect.value);
    form.append("speaker_boost", boostSlider.value);
    form.append("speed", speedSlider.value);
    form.append("temperature", tempSlider.value);

    // Adjust the URL to match your backend route
    const res = await fetch("/api/clone", {
      method: "POST",
      body: form
    });

    if (!res.ok) {
      const msg = await res.text();
      throw new Error(msg || `HTTP ${res.status}`);
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    outputPlayer.src = url;
    downloadLink.href = url;
    statusEl.textContent = "Done.";
  } catch (err) {
    statusEl.textContent = `Error: ${err.message}`;
  } finally {
    generateBtn.disabled = false;
  }
});
