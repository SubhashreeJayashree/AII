require("dotenv").config();
const express = require("express");
const fetch = require("node-fetch");
const http = require("http");
const path = require("path");
const fs = require("fs");
const multer = require("multer");
const FormData = require("form-data");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

const UPLOAD_DIR = path.join(__dirname, "uploads");
if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR);
app.use("/uploads", express.static(UPLOAD_DIR));

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, UPLOAD_DIR),
  filename: (req, file, cb) => cb(null, Date.now() + "-" + (file.originalname || "voice.webm"))
});
const upload = multer({ storage });

app.get("/api/health", (req, res) => res.json({ ok: true }));

async function openaiChat(messages) {
  const key = process.env.OPENAI_API_KEY;
  if (!key) throw new Error("OPENAI_API_KEY not set");
  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: "gpt-3.5-turbo", messages, max_tokens: 800 })
  });
  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error("OpenAI chat error: " + txt);
  }
  const j = await resp.json();
  return j.choices?.[0]?.message?.content || "";
}

app.post("/api/chat", async (req, res) => {
  try {
    const { message, history = [] } = req.body;
    const messages = [
      { role: "system", content: "You are a helpful assistant that mixes social and developer features." },
      ...history,
      { role: "user", content: message }
    ];
    const reply = await openaiChat(messages);
    res.json({ reply });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/api/upload-voice", upload.single("audio"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    const filePath = req.file.path;
    const key = process.env.OPENAI_API_KEY;
    let transcription = null;
    if (key) {
      const form = new FormData();
      form.append("file", fs.createReadStream(filePath));
      form.append("model", "whisper-1");
      const tResp = await fetch("https://api.openai.com/v1/audio/transcriptions", {
        method: "POST",
        headers: { "Authorization": `Bearer ${key}` },
        body: form
      });
      if (tResp.ok) {
        const tj = await tResp.json();
        transcription = tj.text || null;
      } else {
        const txt = await tResp.text();
        console.warn("Transcription failed:", txt);
      }
    }
    let ai_reply = null;
    if (transcription) {
      try {
        ai_reply = await openaiChat([
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: transcription }
        ]);
      } catch (e) {
        console.warn("AI reply failed:", e.message);
      }
    }
    res.json({ file: req.file.filename, transcription, ai_reply, url: "/uploads/" + req.file.filename });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post("/telegram/webhook", async (req, res) => {
  // Minimal placeholder for Telegram updates
  res.json({ ok: true });
});

io.on("connection", (socket) => {
  console.log("socket connected", socket.id);
  socket.on("join-room", (room) => { socket.join(room); socket.to(room).emit("peer-joined", { id: socket.id }); });
  socket.on("signal", (data) => { if (data && data.target) socket.to(data.target).emit("signal", { from: socket.id, signal: data.signal }); });
  socket.on("chat-message", (payload) => { if (payload.room) io.to(payload.room).emit("chat-message", payload); else socket.broadcast.emit("chat-message", payload); });
  socket.on("disconnect", () => socket.broadcast.emit("peer-left", { id: socket.id }));
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server listening on http://localhost:${PORT}`));
