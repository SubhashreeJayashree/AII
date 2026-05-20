const socket = io();
let localStream = null;
let pcMap = {};
const config = (function() {
  const ice = [{ urls: "stun:stun.l.google.com:19302" }];
  return { iceServers: ice };
})();
async function getLocalMedia(constraints = { audio: true, video: true }) {
  localStream = await navigator.mediaDevices.getUserMedia(constraints);
  return localStream;
}
function joinRoom(roomId) { socket.emit("join-room", roomId); }
socket.on("signal", async (data) => {
  const from = data.from; const signal = data.signal;
  if (!pcMap[from]) await createPeerConnection(from, false);
  const pc = pcMap[from];
  if (signal.type === "offer") {
    await pc.setRemoteDescription(new RTCSessionDescription(signal));
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    socket.emit("signal", { target: from, signal: pc.localDescription });
  } else if (signal.type === "answer") {
    await pc.setRemoteDescription(new RTCSessionDescription(signal));
  } else if (signal.candidate) {
    try { await pc.addIceCandidate(new RTCIceCandidate(signal.candidate)); } catch (err) { console.warn(err); }
  }
});
async function createPeerConnection(remoteId, isCaller) {
  const pc = new RTCPeerConnection(config);
  pcMap[remoteId] = pc;
  if (localStream) for (const track of localStream.getTracks()) pc.addTrack(track, localStream);
  pc.onicecandidate = (event) => { if (event.candidate) socket.emit("signal", { target: remoteId, signal: { candidate: event.candidate } }); };
  pc.ontrack = (evt) => {
    let el = document.getElementById("remote-" + remoteId);
    if (!el) { el = document.createElement("video"); el.id = "remote-" + remoteId; el.autoplay = true; el.playsInline = true; el.className = "remote-video"; document.getElementById("remoteContainer")?.appendChild(el) || document.body.appendChild(el); }
    el.srcObject = evt.streams[0];
  };
  pc.onconnectionstatechange = () => { if (pc.connectionState === "disconnected" || pc.connectionState === "failed" || pc.connectionState === "closed") cleanupPeer(remoteId); };
  if (isCaller) { const offer = await pc.createOffer(); await pc.setLocalDescription(offer); socket.emit("signal", { target: remoteId, signal: pc.localDescription }); }
  return pc;
}
function cleanupPeer(remoteId) { const pc = pcMap[remoteId]; if (!pc) return; pc.close(); delete pcMap[remoteId]; const el = document.getElementById("remote-" + remoteId); if (el) el.remove(); }
async function startCallWith(remoteId, opts = { audio: true, video: true }) { await getLocalMedia(opts); let localEl = document.getElementById("localVideo"); if (!localEl) { localEl = document.createElement("video"); localEl.id = "localVideo"; localEl.muted = true; localEl.autoplay = true; localEl.playsInline = true; document.getElementById("localContainer")?.appendChild(localEl) || document.body.appendChild(localEl); } localEl.srcObject = localStream; await createPeerConnection(remoteId, true); }
function hangup() { for (const id of Object.keys(pcMap)) cleanupPeer(id); if (localStream) { for (const t of localStream.getTracks()) t.stop(); localStream = null; const localEl = document.getElementById("localVideo"); if (localEl) localEl.remove(); } }
window.RTC = { joinRoom, startCallWith, hangup, getLocalMedia, socket, localStream };
