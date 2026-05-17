import Anthropic from "@anthropic-ai/sdk";
import { NextRequest, NextResponse } from "next/server";
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
export async function POST(req: NextRequest) {
  const { skill, currentLevel, targetLevel, timeAvailable, learningStyle } = await req.json();
  if (!skill?.trim()) return NextResponse.json({ error: "Skill required" }, { status: 400 });
  const prompt = `You are an expert learning path designer. Create a personalized skill development plan.
Skill: ${skill} | Current level: ${currentLevel || "Beginner"} | Target level: ${targetLevel || "Intermediate"} | Time: ${timeAvailable || "1 hour/day"} | Style: ${learningStyle || "Hands-on"}
Return JSON: { "skillName": "string", "estimatedTime": "string", "milestones": [{ "title": "string", "duration": "string", "topics": ["string"], "projects": ["string"], "resources": ["string"] }], "dailyPlan": [{ "day": "string", "focus": "string", "activities": ["string"], "time": "string" }], "keyResources": [{ "title": "string", "type": "Book|Course|Video|Practice", "url": "string", "why": "string" }], "commonMistakes": ["string"], "checkpoints": ["string"], "careerApplications": ["string"], "summary": "string" }
Return ONLY valid JSON.`;
  try {
    const msg = await client.messages.create({ model: "claude-sonnet-4-6", max_tokens: 1800, messages: [{ role: "user", content: prompt }] });
    return NextResponse.json(JSON.parse((msg.content[0] as { type: string; text: string }).text));
  } catch (e) { return NextResponse.json({ error: String(e) }, { status: 500 }); }
}
