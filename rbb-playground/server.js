// RBB hash playground — paste paragraphs, get MD5 -> BIP39 -> BIP44 m/44'/0'/0'/0/i P2PKH.
// Certified against the author's own published vectors on boot (see /api/selftest).
import express from "express";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { HDKey } from "@scure/bip32";
import { entropyToMnemonic, mnemonicToSeedSync } from "@scure/bip39";
import { wordlist } from "@scure/bip39/wordlists/english";
import { sha256 } from "@noble/hashes/sha256";
import { ripemd160 } from "@noble/hashes/ripemd160";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(express.json({ limit: "4mb" }));
app.use(express.static(path.join(__dirname, "public")));

// ---- the addresses this hunt cares about ----
const TARGETS = {
  "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN": "Stage One escrow (solved/swept — a control)",
  "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "RBB pre-rehash escrow (dead, one line break)",
  "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "RBB LIVE escrow — 0.777 BTC (two line breaks)",
};

// ---- crypto helpers ----
const B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
function base58(buf) {
  let n = BigInt("0x" + Buffer.from(buf).toString("hex"));
  let out = "";
  while (n > 0n) { const r = n % 58n; n = n / 58n; out = B58[Number(r)] + out; }
  for (const b of buf) { if (b === 0) out = "1" + out; else break; }
  return out;
}
function base58check(payload) {
  const chk = sha256(sha256(payload)).slice(0, 4);
  return base58(Buffer.concat([Buffer.from(payload), Buffer.from(chk)]));
}
function p2pkhFromPub(pub) {
  const h = ripemd160(sha256(pub));
  return base58check(Buffer.concat([Buffer.from([0x00]), Buffer.from(h)]));
}
function wifFromPriv(priv, compressed = true) {
  const body = compressed
    ? Buffer.concat([Buffer.from([0x80]), Buffer.from(priv), Buffer.from([0x01])])
    : Buffer.concat([Buffer.from([0x80]), Buffer.from(priv)]);
  return base58check(body);
}

// entropy (16 bytes) -> account node m/44'/0'/0'/0
function accountFromEntropy(entropy) {
  const mnemonic = entropyToMnemonic(entropy, wordlist);
  const seed = mnemonicToSeedSync(mnemonic, "");
  const root = HDKey.fromMasterSeed(seed);
  const acct = root.derive("m/44'/0'/0'/0");
  return { mnemonic, acct };
}
function deriveFromEntropy(entropy, n = 6) {
  const { mnemonic, acct } = accountFromEntropy(entropy);
  const rows = [];
  for (let i = 0; i < n; i++) {
    const child = acct.deriveChild(i);
    const address = p2pkhFromPub(child.publicKey);
    rows.push({
      index: i,
      address,
      wif: wifFromPriv(child.privateKey, true),
      target: TARGETS[address] || null,
    });
  }
  return { mnemonic, rows };
}

function md5hex(text) {
  return crypto.createHash("md5").update(Buffer.from(text, "utf8")).digest("hex");
}

// ---- separators / carrier assembly ----
const SEP = { LFLF: "\n\n", CRLFCRLF: "\r\n\r\n", LF: "\n", CRLF: "\r\n", SPACE: " ", NONE: "" };

// split pasted text into paragraphs on blank lines
function splitParagraphs(text) {
  return text.replace(/\r\n/g, "\n").split(/\n[ \t]*\n+/).map((p) => p.replace(/\n/g, " ").trimEnd()).filter((p) => p.length > 0);
}

// ---- API ----
app.post("/api/hash", (req, res) => {
  try {
    const { text = "", sepKey = "CRLFCRLF", indices = 8, mode = "raw" } = req.body || {};
    let carrier;
    let paragraphs = null;
    if (mode === "paragraphs") {
      paragraphs = splitParagraphs(text);
      const sep = SEP[sepKey] ?? "\r\n\r\n";
      carrier = paragraphs.join(sep);
    } else {
      // raw: hash exactly what was pasted (still normalize the chosen line-ending if asked)
      carrier = text;
      if (sepKey === "CRLFCRLF" || sepKey === "CRLF") carrier = carrier.replace(/\r?\n/g, sepKey === "CRLF" ? "\r\n" : "\r\n");
      else carrier = carrier.replace(/\r\n/g, "\n");
    }
    const md5 = md5hex(carrier);
    const entropy = Uint8Array.from(Buffer.from(md5, "hex"));
    const { mnemonic, rows } = deriveFromEntropy(entropy, Math.min(Math.max(1, indices | 0), 50));
    const hit = rows.find((r) => r.address === "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W" || r.address === "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC");
    const perParagraph = (paragraphs || splitParagraphs(text)).map((p, i) => ({
      i,
      md5: md5hex(p),
      len: p.length,
      first: (p.match(/[A-Za-z]/) || ["?"])[0],
      last: (p.match(/[A-Za-z](?=[^A-Za-z]*$)/) || ["?"])[0],
      preview: p.slice(0, 70),
    }));
    res.json({ ok: true, bytes: Buffer.byteLength(carrier, "utf8"), md5, mnemonic, rows, perParagraph, hit: !!hit });
  } catch (e) {
    res.status(400).json({ ok: false, error: String(e && e.message ? e.message : e) });
  }
});

// derive straight from an entropy/MD5 hex (power tool)
app.post("/api/entropy", (req, res) => {
  try {
    let { hex = "", indices = 8 } = req.body || {};
    hex = String(hex).trim().toLowerCase().replace(/[^0-9a-f]/g, "");
    if (hex.length !== 32) throw new Error("entropy must be 32 hex chars (16 bytes / an MD5)");
    const entropy = Uint8Array.from(Buffer.from(hex, "hex"));
    const { mnemonic, rows } = deriveFromEntropy(entropy, Math.min(Math.max(1, indices | 0), 50));
    res.json({ ok: true, md5: hex, mnemonic, rows });
  } catch (e) {
    res.status(400).json({ ok: false, error: String(e && e.message ? e.message : e) });
  }
});

// boot self-test: certified vectors must reproduce
function selftest() {
  const out = {};
  // Stage One: entropy 9dd2efb9... idx0 -> 19Tby...
  const s1 = deriveFromEntropy(Uint8Array.from(Buffer.from("9dd2efb9bc976c2095bd534d7b8d431c", "hex")), 1);
  out.stageOne = {
    got: s1.rows[0].address,
    want: "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN",
    pass: s1.rows[0].address === "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN",
  };
  // Author's published WIF vector: entropy 2941774a... idx1 -> L5Z66...
  const v = deriveFromEntropy(Uint8Array.from(Buffer.from("2941774a2abec9f30c7d6777d1d53d91", "hex")), 2);
  out.wifVector = {
    got: v.rows[1].wif,
    want: "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex",
    pass: v.rows[1].wif === "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex",
  };
  out.pass = out.stageOne.pass && out.wifVector.pass;
  return out;
}
let SELFTEST = { pass: false };
try { SELFTEST = selftest(); } catch (e) { SELFTEST = { pass: false, error: String(e) }; }
app.get("/api/selftest", (_req, res) => res.json(SELFTEST));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`RBB hash playground on :${PORT}  |  derivation self-test: ${SELFTEST.pass ? "PASS ✅" : "FAIL ❌"}`);
});
