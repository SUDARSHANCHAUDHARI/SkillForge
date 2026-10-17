import { NextRequest, NextResponse } from "next/server";

// Dependency-free in-memory rate limiter + request guards.
// NOTE: in-memory state is per-instance. On multi-instance/serverless deploys,
// swap in a shared store (e.g. @upstash/ratelimit) — the call sites stay the same.

// A missing or non-numeric env value falls back to the default instead of disabling the guard.
function envInt(name: string, fallback: number): number {
  const n = Number(process.env[name]);
  return Number.isFinite(n) && n > 0 ? n : fallback;
}

const WINDOW_MS = envInt("RATE_LIMIT_WINDOW_MS", 60_000);
const MAX_REQ = envInt("RATE_LIMIT_MAX", 20);
const MAX_BODY = envInt("MAX_BODY_BYTES", 100_000); // ~100KB: these routes take text only

type Bucket = { count: number; reset: number };
const buckets = new Map<string, Bucket>();

// The client can put anything at the front of x-forwarded-for; the last entry is the one the
// nearest proxy appended. Prefer x-real-ip, which hosts such as Vercel set themselves.
function clientIp(req: NextRequest): string {
  const real = req.headers.get("x-real-ip")?.trim();
  if (real) return real;
  const xff = req.headers.get("x-forwarded-for");
  if (xff) return xff.split(",").at(-1)!.trim();
  return "unknown";
}

export function rateLimit(req: NextRequest): NextResponse | null {
  const now = Date.now();
  const ip = clientIp(req);
  const b = buckets.get(ip);
  if (!b || now > b.reset) {
    buckets.set(ip, { count: 1, reset: now + WINDOW_MS });
  } else if (++b.count > MAX_REQ) {
    return NextResponse.json(
      { error: "Rate limit exceeded. Try again later." },
      { status: 429, headers: { "Retry-After": String(Math.ceil((b.reset - now) / 1000)) } },
    );
  }
  if (buckets.size > 10_000) for (const [k, v] of buckets) if (now > v.reset) buckets.delete(k);
  return null;
}

// Rate-limit + declared payload-size gate. Call at the top of every handler.
export function guard(req: NextRequest): NextResponse | null {
  const rl = rateLimit(req);
  if (rl) return rl;
  const len = Number(req.headers.get("content-length") ?? 0);
  if (len > MAX_BODY) return tooLarge();
  return null;
}

function tooLarge(): NextResponse {
  return NextResponse.json({ error: "Payload too large" }, { status: 413 });
}

// Read and parse the JSON body, stopping at MAX_BODY bytes even when content-length is absent.
// Returns the parsed body (untyped, like req.json()), or a 413/400 response to send back.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function readJson<T = any>(req: NextRequest): Promise<T | NextResponse> {
  if (!req.body) return NextResponse.json({ error: "Request body required" }, { status: 400 });
  const reader = req.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > MAX_BODY) {
      await reader.cancel();
      return tooLarge();
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const c of chunks) {
    bytes.set(c, offset);
    offset += c.byteLength;
  }
  try {
    const data: unknown = JSON.parse(new TextDecoder().decode(bytes));
    if (typeof data !== "object" || data === null || Array.isArray(data)) throw new Error("not an object");
    return data as T;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
}

// Generic 500 that never leaks internals; logs server-side only.
export function safeError(e: unknown): NextResponse {
  console.error("[api] error:", e);
  return NextResponse.json({ error: "Internal server error" }, { status: 500 });
}

type Block = { type: string; text?: string };
// Safely pull the first text block from an Anthropic message; throws (-> safeError) if none.
export function extractText(msg: { content: Block[] }): string {
  const block = msg.content.find((b) => b.type === "text" && typeof b.text === "string");
  if (!block?.text) throw new Error("model response contained no text block");
  return block.text;
}

// Parse model JSON, tolerating ```json fences. Throws (-> safeError) on invalid JSON.
export function safeJson<T = unknown>(text: string): T {
  const cleaned = text.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "").trim();
  return JSON.parse(cleaned) as T;
}
