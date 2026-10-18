"use client";
import { useState } from "react";

const LEVELS = ["Complete Beginner", "Some Experience", "Intermediate", "Advanced"];
const GOALS = ["Career Change", "Side Project", "Academic", "Freelance", "Curiosity"];
const HOURS_PER_DAY = ["0.5h", "1h", "2h", "3h", "4h+"];
const TABS = ["milestones", "daily_plan", "resources", "checkpoints"];
const TAB_LABELS: Record<string, string> = { milestones: "Milestones", daily_plan: "Daily Plan", resources: "Resources", checkpoints: "Checkpoints" };

// Shape matches the JSON the prompt in app/api/generate/route.ts asks for.
interface Milestone { title: string; duration: string; topics: string[]; projects: string[]; resources: string[]; }
interface DaySlot { day: string; focus: string; activities: string[]; time: string; }
interface Resource { title: string; type: string; url: string; why: string; }
interface SkillResult {
  summary?: string;
  estimatedTime?: string;
  milestones?: Milestone[];
  dailyPlan?: DaySlot[];
  keyResources?: Resource[];
  checkpoints?: string[];
}

export default function SkillForgePage() {
  const [skill, setSkill] = useState("");
  const [level, setLevel] = useState("Complete Beginner");
  const [goal, setGoal] = useState("Career Change");
  const [hoursPerDay, setHoursPerDay] = useState("1h");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SkillResult | null>(null);
  const [activeTab, setActiveTab] = useState("milestones");
  const [error, setError] = useState("");

  async function generate() {
    if (!skill.trim()) return;
    setLoading(true); setError("");
    try {
      const res = await fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ skill, level, goal, hoursPerDay }) });
      const data = await res.json();
      if (data.error) setError(data.error); else setResult(data as SkillResult);
    } catch (e) { setError(String(e)); }
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-orange-400 mb-2">SkillForge</h1>
          <p className="text-slate-500">Generate a personalized learning path for any skill — milestones, daily plans, and resources</p>
        </div>
        <div className="mb-4">
          <label className="block text-sm text-slate-400 mb-2">What skill do you want to learn?</label>
          <input className="w-full bg-[#111118] border border-orange-900 rounded-lg px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-orange-600" placeholder="e.g. Machine Learning, Guitar, React, Data Analysis, Spanish..." value={skill} onChange={(e) => setSkill(e.target.value)} />
        </div>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm text-slate-400 mb-2">Current Level</label>
            <div className="space-y-1">{LEVELS.map((l) => <button key={l} onClick={() => setLevel(l)} className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${level === l ? "bg-orange-800/50 text-orange-200 border border-orange-600" : "bg-[#111118] text-slate-400 border border-slate-700 hover:border-orange-900"}`}>{l}</button>)}</div>
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-2">Learning Goal</label>
            <div className="space-y-1">{GOALS.map((g) => <button key={g} onClick={() => setGoal(g)} className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${goal === g ? "bg-orange-800/50 text-orange-200 border border-orange-600" : "bg-[#111118] text-slate-400 border border-slate-700 hover:border-orange-900"}`}>{g}</button>)}</div>
          </div>
        </div>
        <div className="mb-6">
          <label className="block text-sm text-slate-400 mb-2">Hours per Day</label>
          <div className="flex gap-2">{HOURS_PER_DAY.map((h) => <button key={h} onClick={() => setHoursPerDay(h)} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${hoursPerDay === h ? "bg-orange-800 text-orange-200 border border-orange-600" : "bg-[#111118] text-slate-400 border border-slate-700 hover:border-orange-900"}`}>{h}</button>)}</div>
        </div>
        <button onClick={generate} disabled={loading || !skill.trim()} className="px-6 py-2 bg-orange-700 hover:bg-orange-600 disabled:opacity-40 text-white rounded-lg text-sm font-medium transition-colors mb-6">{loading ? "Generating..." : "Forge Learning Path"}</button>
        {error && <div className="p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-400 text-sm mb-4">{error}</div>}
        {result && (
          <div>
            {(result.summary || result.estimatedTime) && (
              <div className="bg-[#111118] border border-orange-900/30 rounded-xl p-4 mb-4">
                <div className="flex items-center gap-4 text-sm">
                  {result.estimatedTime && <span className="text-orange-300 font-semibold">{result.estimatedTime}</span>}
                  {result.summary && <><span className="text-slate-600">·</span><span className="text-slate-400">{result.summary}</span></>}
                </div>
              </div>
            )}
            <div className="bg-[#111118] border border-slate-700 rounded-xl overflow-hidden">
              <div className="flex border-b border-slate-700">
                {TABS.map((t) => <button key={t} onClick={() => setActiveTab(t)} className={`px-5 py-3 text-sm font-medium transition-colors ${activeTab === t ? "text-orange-300 border-b-2 border-orange-500" : "text-slate-500 hover:text-slate-300"}`}>{TAB_LABELS[t]}</button>)}
              </div>
              <div className="p-5">
                {activeTab === "milestones" && result.milestones?.map((m, i) => (
                  <div key={i} className="flex gap-4 items-start p-3 bg-[#0d0d14] rounded-lg mb-2">
                    <div className="w-10 h-10 rounded-full bg-orange-900/40 border border-orange-700 flex items-center justify-center text-orange-300 text-sm font-bold flex-shrink-0">{i + 1}</div>
                    <div>
                      <h4 className="text-slate-200 font-medium text-sm">{m.title}</h4>
                      <p className="text-slate-500 text-xs mt-0.5">{m.duration}</p>
                      <p className="text-slate-400 text-sm mt-1">{m.topics?.join(", ")}</p>
                    </div>
                  </div>
                ))}
                {activeTab === "daily_plan" && result.dailyPlan?.map((item, i) => (
                  <div key={i} className="flex gap-4 items-center p-3 bg-[#0d0d14] rounded-lg mb-2">
                    <span className="text-orange-400 text-xs font-mono w-12">{item.day}</span>
                    <span className="text-slate-300 text-sm flex-1">{item.focus}: {item.activities?.join(", ")}</span>
                    <span className="text-slate-600 text-xs">{item.time}</span>
                  </div>
                ))}
                {activeTab === "resources" && result.keyResources?.map((r, i) => (
                  <div key={i} className="flex gap-3 items-start p-3 bg-[#0d0d14] rounded-lg mb-2">
                    <span className="px-2 py-0.5 bg-orange-900/30 text-orange-500 text-xs rounded mt-0.5">{r.type}</span>
                    <div>
                      <p className="text-slate-200 text-sm font-medium">{r.title}</p>
                      <p className="text-slate-500 text-xs mt-0.5">{r.why}</p>
                    </div>
                  </div>
                ))}
                {activeTab === "checkpoints" && result.checkpoints?.map((c, i) => (
                  <div key={i} className="flex gap-3 items-start p-3 bg-[#0d0d14] rounded-lg mb-2">
                    <input type="checkbox" className="mt-1 accent-orange-500" readOnly />
                    <p className="text-slate-200 text-sm">{c}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
