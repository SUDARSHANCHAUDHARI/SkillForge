import Anthropic from "@anthropic-ai/sdk";
import { guard, readJson, safeError, extractText, safeJson } from "../../../lib/apiGuard";
import { NextRequest, NextResponse } from "next/server";
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
export async function POST(req: NextRequest) {
  const _guard = guard(req);
  if (_guard) return _guard;
  const body = await readJson(req);
  if (body instanceof NextResponse) return body;
  const { skill, level, targetLevel, goal, hoursPerDay } = body;
  if (!skill?.trim()) return NextResponse.json({ error: "Skill required" }, { status: 400 });
  const prompt = `You are an expert learning path designer. Create a personalized skill development plan.
Skill: ${skill} | Current level: ${level || "Complete Beginner"} | Target level: ${targetLevel || "Intermediate"} | Goal: ${goal || "Curiosity"} | Time: ${hoursPerDay ? `${hoursPerDay}/day` : "1h/day"}
Return JSON: { "skillName": "string", "estimatedTime": "string", "milestones": [{ "title": "string", "duration": "string", "topics": ["string"], "projects": ["string"], "resources": ["string"] }], "dailyPlan": [{ "day": "string", "focus": "string", "activities": ["string"], "time": "string" }], "keyResources": [{ "title": "string", "type": "Book|Course|Video|Practice", "url": "string", "why": "string" }], "commonMistakes": ["string"], "checkpoints": ["string"], "careerApplications": ["string"], "summary": "string" }
Return ONLY valid JSON.`;
  try {
    const msg = await client.messages.create({ model: "claude-sonnet-4-6", max_tokens: 1800, messages: [{ role: "user", content: prompt }] });
    return NextResponse.json(safeJson(extractText(msg)));
  } catch (e) { return safeError(e); }
}
