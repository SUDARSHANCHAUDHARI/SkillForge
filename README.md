# SkillForge 🔨📚

**Generate a personalized skill development learning path — milestones, daily plan, curated resources, checkpoints, and career applications, all from a single skill input.**

Enter a skill, your current level, target level, available time per day, and learning style, and get a complete learning roadmap: estimated total time, phased milestones with topics and projects, a day-by-day plan, key resources (books/courses/videos/practice), common mistakes, checkpoints to validate progress, and career applications.

---

## Table of Contents

- [🌟 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🖥️ UI Overview](#-ui-overview)
- [🚀 Getting Started](#-getting-started)
- [📜 Scripts](#-scripts)
- [🔑 Environment Variables](#-environment-variables)
- [📊 Current Status](#-current-status)
- [🛠️ Tech Stack](#-tech-stack)
- [🔒 Security](#-security)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)
- [About](#about)

## 🌟 Features

### 🔨 Core Features
- ✅ **Skill Input** — any skill (e.g. "TypeScript", "Public Speaking", "Machine Learning")
- ✅ **Current Level Selector** — Complete Beginner, Some Experience, Intermediate, Advanced
- ✅ **Target Level Selector** — Some Experience, Intermediate, Advanced, Expert
- ✅ **Goal Selector** — Career Change, Side Project, Academic, Freelance, Curiosity
- ✅ **Hours Per Day** — 0.5h, 1h, 2h, 3h, 4h+
- ✅ **Estimated Total Time** — how long to reach the target level
- ✅ **Milestones Tab** — phased milestones with title, duration, week, topics, projects, resources
- ✅ **Daily Plan Tab** — day-by-day schedule with focus area, activities, time allocation
- ✅ **Resources Tab** — curated books, courses, videos, and practice resources with why-this rationale
- ✅ **Checkpoints Tab** — validation checkpoints with test criteria
- ✅ **Common Mistakes** — pitfalls to avoid for this specific skill
- ✅ **Career Applications** — how this skill applies in professional contexts
- ✅ **Summary** — one-paragraph learning path overview

### 🤖 AI Features
- ✅ **Claude Sonnet 4.6** — designs evidence-based, personalized learning paths
- ✅ **Level-calibrated** — Complete Beginner path differs structurally from Advanced → Expert
- ✅ **Time-aware** — daily plan adapts to 0.5h vs 4h+ availability
- ✅ **Goal-informed** — Career Change paths emphasize portfolio projects; Curiosity paths favor exploration
- ✅ **Resource specificity** — recommends real, named resources with rationale

### ⚙️ Technical Features
- ✅ **Next.js 15 App Router** — server + client components
- ✅ **TypeScript strict mode** — fully typed milestone and resource interfaces
- ✅ **Tailwind CSS** — dark violet theme with tabbed result panel

---

## 🏗️ Architecture

```
SkillForge/
├── 📁 app/
│   ├── 📄 page.tsx          # Main UI — skill input + tabbed learning path
│   ├── 📄 layout.tsx        # Root layout with dark background
│   ├── 📄 globals.css       # Global styles
│   └── 📁 api/
│       └── 📁 generate/
│           └── 📄 route.ts  # POST /api/generate — Claude learning path designer
├── 📁 public/               # Static assets
├── 📄 .env.example          # Environment variable template
├── 📄 package.json
└── 📄 README.md
```

---

## 🖥️ UI Overview

| Section | Description |
|---|---|
| **Skill Input** | Free-text — any skill to learn |
| **Current Level** | Chips — Complete Beginner through Advanced |
| **Target Level** | Chips — Some Experience through Expert |
| **Goal** | Chips — Career Change, Side Project, Academic, Freelance, Curiosity |
| **Hours Per Day** | Chips — 0.5h to 4h+ |
| **Generate Path** | Triggers Claude learning path generation |
| **Estimated Time** | Total duration to reach target level |
| **Summary** | One-paragraph overview |
| **Milestones Tab** | Phased milestones with topics and projects |
| **Daily Plan Tab** | Day-by-day schedule |
| **Resources Tab** | Curated books, courses, videos, practice |
| **Checkpoints Tab** | Validation criteria for each phase |
| **Common Mistakes** | Pitfalls specific to this skill |
| **Career Applications** | Professional use cases |

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- pnpm
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SUDARSHANCHAUDHARI/SkillForge.git
   cd SkillForge
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env.local
   # Edit .env.local and add your ANTHROPIC_API_KEY
   ```

4. **Run dev server**
   ```bash
   pnpm dev
   ```
   Open [http://localhost:3000](http://localhost:3000)

---

## 📜 Scripts

```bash
pnpm dev      # Start development server (Turbopack)
pnpm build    # Production build
pnpm start    # Start production server
pnpm lint     # ESLint check
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ✅ Yes |

Get your key at [console.anthropic.com](https://console.anthropic.com). Add it to `.env.local` — this file is gitignored and never committed.

---

## 📊 Current Status

| Property | Value |
|---|---|
| **Version** | 1.0.0 |
| **Status** | ✅ MVP Complete |
| **Model** | claude-sonnet-4-6 |
| **Skill Levels** | 4 (Complete Beginner, Some Experience, Intermediate, Advanced) |
| **Goals** | 5 (Career Change, Side Project, Academic, Freelance, Curiosity) |
| **Time Options** | 5 (0.5h, 1h, 2h, 3h, 4h+) |
| **Result Tabs** | 4 (Milestones, Daily Plan, Resources, Checkpoints) |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Framework** | Next.js 15 (App Router) |
| **Language** | TypeScript (strict mode) |
| **Styling** | Tailwind CSS |
| **AI** | Claude API — claude-sonnet-4-6 |
| **Package Manager** | pnpm |

---

## 🔒 Security

- `ANTHROPIC_API_KEY` lives in `.env.local` — gitignored, never committed
- `.env.example` contains placeholder values only
- API key sent directly to Anthropic — no intermediate server
- Skill inputs not stored or logged server-side

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feat/your-feature`)
5. Open a Pull Request

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/SUDARSHANCHAUDHARI/SkillForge/issues)

---

<div align="center">

**Made with ❤️ by [SUDARSHANCHAUDHARI](https://github.com/SUDARSHANCHAUDHARI)**

[⭐ Star this repo](https://github.com/SUDARSHANCHAUDHARI/SkillForge) · [🐛 Report Issue](https://github.com/SUDARSHANCHAUDHARI/SkillForge/issues)

</div>

---

## About

I'm Sudarshan Chaudhari, a Senior Quality Engineer, Test Automation specialist, and AI systems builder based in Bangkok, Thailand.

I have 13+ years of experience in software quality engineering, working across SaaS, fintech, gaming, web, mobile, cloud, and digital signage platforms. My background combines hands-on test automation with QA leadership, test strategy, CI/CD, release quality, production investigation, and cross-platform validation.

Alongside my professional QA career, I run [SudarshanTechLabs](https://sudarshantechlabs.com/), my independent engineering and product lab where I design, build, test, and ship software across Android, web, AI, cybersecurity, developer tooling, and cross-platform applications.

### What I work on

- ⚙️ **Quality Engineering & Test Automation** — Playwright, Selenium, Cypress, Appium, API testing, automation frameworks, end-to-end testing, CI/CD, release gates, GitHub Actions, risk-based testing, and production validation
- 🤖 **AI Systems & Automation** — AI agents, multi-agent orchestration, MCP servers, AI-assisted QA, prompt tooling, developer workflows, automation systems, and Claude Code plugins
- 📱 **Mobile & Cross-Platform Applications** — Android applications built with Kotlin and Jetpack Compose, Google Play releases, automated build and publishing pipelines, and cross-platform development spanning iOS, web, Windows, and macOS
- 🌐 **Web Applications & Platforms** — Full-stack applications using Next.js, TypeScript, Firebase, Cloudflare, REST APIs, and modern web infrastructure
- 🛠️ **Developer Tooling & CLI Engineering** — Rust, Python, TypeScript, CLI utilities, multi-repository tooling, build automation, release tooling, and engineering productivity systems
- 🛡️ **Cybersecurity & Observability** — Threat detection, log analysis, security auditing, vulnerability assessment, monitoring, and security-focused developer tools
- 📺 **Digital Signage & Device Platforms** — Content validation, playback testing, device compatibility, production investigation, monitoring, and QA across diverse hardware and operating-system environments

My work sits at the intersection of quality engineering, automation, AI, and software development. I approach products with a QA mindset from the beginning: understanding failure modes, designing for testability, automating repetitive work, and building release confidence into the engineering process.

Through SudarshanTechLabs, I also build products and tools from idea to production, covering architecture, development, testing, CI/CD, release automation, monitoring, and ongoing maintenance.

🌐 [sudarshantechlabs.com](https://sudarshantechlabs.com/) · 💼 [LinkedIn](https://linkedin.com/in/sudarshan-chaudhari) · 🐙 [GitHub](https://github.com/SUDARSHANCHAUDHARI) · ✉️ [sunny.sudarshan@gmail.com](mailto:sunny.sudarshan@gmail.com)
