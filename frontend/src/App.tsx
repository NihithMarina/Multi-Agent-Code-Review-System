import { useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { BarChart3, Bot, CheckCircle2, Shield, Sparkles, Workflow } from 'lucide-react'
import { getAnalytics, getHealth } from './lib/api'
import type { AnalyticsOverview } from './types'

const pipeline = [
  { name: 'Security', tone: 'critical', detail: 'Secrets, injection, auth bypasses, and unsafe execution.' },
  { name: 'Performance', tone: 'high', detail: 'Hot paths, allocations, N+1 access, and unnecessary work.' },
  { name: 'Clean Code', tone: 'medium', detail: 'Readability, naming, structure, and maintainability.' },
  { name: 'Testing', tone: 'high', detail: 'Coverage gaps, edge cases, and regression risk.' },
  { name: 'Documentation', tone: 'low', detail: 'API notes, onboarding clarity, and developer guidance.' },
  { name: 'Dependency', tone: 'medium', detail: 'Package changes, supply-chain risk, and compatibility.' },
  { name: 'Architecture', tone: 'high', detail: 'Layer boundaries, coupling, and design drift.' },
]

const reviewHistory = [
  { pr: '#2481', repo: 'payments-service', status: 'Resolved', severity: 'high', title: 'Replace broad DB query with projection' },
  { pr: '#2477', repo: 'platform-api', status: 'Posted', severity: 'critical', title: 'Remove unsafely interpolated SQL' },
  { pr: '#2463', repo: 'mobile-web', status: 'Queued', severity: 'medium', title: 'Add tests for retry flow' },
]

function App() {
  const [health, setHealth] = useState('connecting')
  const [analytics, setAnalytics] = useState<AnalyticsOverview | null>(null)

  useEffect(() => {
    let mounted = true

    getHealth()
      .then(() => {
        if (mounted) setHealth('online')
      })
      .catch(() => {
        if (mounted) setHealth('offline')
      })

    getAnalytics()
      .then((payload) => {
        if (mounted) setAnalytics(payload)
      })
      .catch(() => {
        if (mounted) setAnalytics(null)
      })

    return () => {
      mounted = false
    }
  }, [])

  return (
    <div className="min-h-screen bg-ink-950 text-white">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute left-[-12rem] top-[-10rem] h-[30rem] w-[30rem] rounded-full bg-aurora-cyan/20 blur-3xl" />
        <div className="absolute right-[-8rem] top-[8rem] h-[28rem] w-[28rem] rounded-full bg-aurora-coral/10 blur-3xl" />
        <div className="absolute bottom-[-10rem] left-[40%] h-[24rem] w-[24rem] rounded-full bg-aurora-mint/10 blur-3xl" />
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] bg-[size:64px_64px] opacity-30" />
      </div>

      <main className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-6 sm:px-6 lg:px-8">
        <header className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-glow backdrop-blur-xl sm:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.24em] text-white/70">
                <Sparkles className="h-3.5 w-3.5 text-aurora-mint" />
                Enterprise AI Code Review Platform
              </div>
              <h1 className="font-display text-4xl leading-tight font-semibold tracking-tight text-white sm:text-6xl">
                CodeGuardian AI keeps pull requests moving without losing review rigor.
              </h1>
              <p className="max-w-2xl text-sm leading-7 text-white/70 sm:text-base">
                Seven specialized agents inspect every change, a coordinator consolidates findings, and the platform can post polished comments back to GitHub with organizational standards baked in.
              </p>
            </div>

            <div className="grid min-w-[260px] gap-3 rounded-3xl border border-white/10 bg-ink-900/70 p-4">
              <Metric label="Backend" value={health === 'online' ? 'Connected' : health === 'offline' ? 'Offline' : 'Checking'} accentClass="bg-aurora-mint" />
              <Metric label="Agents" value="7 specialized reviewers" accentClass="bg-aurora-cyan" />
              <Metric label="Platform" value="FastAPI + LangGraph" accentClass="bg-aurora-gold" />
            </div>
          </div>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <StatCard icon={<Shield className="h-5 w-5" />} title="Security posture" value={analytics?.findings_by_severity?.critical ?? 12} note="Critical issues surfaced this week" />
          <StatCard icon={<Workflow className="h-5 w-5" />} title="Review throughput" value={analytics?.total_reviews ?? 128} note="Reviews processed across teams" />
          <StatCard icon={<BarChart3 className="h-5 w-5" />} title="Active queue" value={analytics?.open_reviews ?? 9} note="Open reviews awaiting action" />
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
          <Panel title="Agent pipeline" subtitle="Each PR passes through a coordinated review graph before comments are posted.">
            <div className="grid gap-3 lg:grid-cols-2">
              {pipeline.map((agent, index) => (
                <div key={agent.name} className="rounded-2xl border border-white/10 bg-ink-900/80 p-4 transition hover:-translate-y-0.5 hover:border-white/20">
                  <div className="mb-3 flex items-center justify-between gap-2">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/8 text-sm font-semibold text-white/80">0{index + 1}</div>
                      <div>
                        <p className="font-medium text-white">{agent.name}</p>
                        <p className="text-xs uppercase tracking-[0.2em] text-white/40">{agent.tone} priority</p>
                      </div>
                    </div>
                    <Bot className="h-5 w-5 text-aurora-cyan" />
                  </div>
                  <p className="text-sm leading-6 text-white/65">{agent.detail}</p>
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="Review history" subtitle="Recent decisions and their current state.">
            <div className="space-y-3">
              {reviewHistory.map((item) => (
                <article key={item.pr} className="rounded-2xl border border-white/10 bg-ink-900/80 p-4">
                  <div className="mb-2 flex items-center justify-between gap-3">
                    <div>
                      <p className="font-medium text-white">{item.title}</p>
                      <p className="text-xs text-white/45">{item.repo} · {item.pr}</p>
                    </div>
                    <span className={badgeClass(item.status)}>{item.status}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm text-white/60">
                    <span>Severity</span>
                    <span className="capitalize text-white">{item.severity}</span>
                  </div>
                </article>
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <Panel title="Findings by severity" subtitle="Aggregated analytics from the platform API.">
            <div className="space-y-4">
              {(['critical', 'high', 'medium', 'low'] as const).map((severity) => {
                const value = analytics?.findings_by_severity?.[severity] ?? 0
                return (
                  <div key={severity} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="capitalize text-white/70">{severity}</span>
                      <span className="text-white">{value}</span>
                    </div>
                    <div className="h-2 rounded-full bg-white/10">
                      <div className={`h-2 rounded-full ${severityBar(severity)}`} style={{ width: `${Math.min(100, Math.max(10, value * 12))}%` }} />
                    </div>
                  </div>
                )
              })}
            </div>
          </Panel>

          <Panel title="Review intelligence" subtitle="RAG and semantic search prepare the platform for organization-specific guidance.">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-2xl border border-white/10 bg-ink-900/80 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-white/40">RAG corpus</p>
                <p className="mt-2 text-2xl font-semibold text-white">FAISS + Sentence Transformers</p>
                <p className="mt-2 text-sm leading-6 text-white/65">Standards documents are embedded, indexed, and retrieved into the review graph before the agents render their comments.</p>
              </div>
              <div className="rounded-2xl border border-white/10 bg-ink-900/80 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-white/40">History search</p>
                <p className="mt-2 text-2xl font-semibold text-white">Semantic replay</p>
                <p className="mt-2 text-sm leading-6 text-white/65">Review artifacts and outcomes can be searched by meaning, enabling faster triage of repeated findings.</p>
              </div>
            </div>
            <div className="mt-4 rounded-2xl border border-aurora-cyan/20 bg-aurora-cyan/10 p-4 text-sm leading-6 text-white/80">
              The backend is designed to post comments back to GitHub only when the operator enables it, keeping approval and rollout under control.
            </div>
          </Panel>
        </section>
      </main>
    </div>
  )
}

function Metric({ label, value, accentClass }: { label: string; value: string; accentClass: string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
      <p className="text-xs uppercase tracking-[0.22em] text-white/45">{label}</p>
      <p className={`mt-1 text-lg font-semibold text-white`}>
        <span className={`mr-2 inline-block h-2.5 w-2.5 rounded-full ${accentClass}`} />
        {value}
      </p>
    </div>
  )
}

function Panel({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) {
  return (
    <section className="rounded-[2rem] border border-white/10 bg-white/5 p-5 shadow-glow backdrop-blur-xl sm:p-6">
      <div className="mb-5">
        <h2 className="font-display text-2xl font-semibold text-white">{title}</h2>
        <p className="mt-1 text-sm leading-6 text-white/60">{subtitle}</p>
      </div>
      {children}
    </section>
  )
}

function StatCard({ icon, title, value, note }: { icon: ReactNode; title: string; value: number; note: string }) {
  return (
    <article className="rounded-[1.75rem] border border-white/10 bg-white/5 p-5 shadow-glow backdrop-blur-xl">
      <div className="mb-6 flex items-center justify-between">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3 text-aurora-cyan">{icon}</div>
        <CheckCircle2 className="h-5 w-5 text-aurora-mint" />
      </div>
      <p className="text-sm uppercase tracking-[0.22em] text-white/45">{title}</p>
      <p className="mt-2 text-4xl font-semibold text-white">{value}</p>
      <p className="mt-2 text-sm leading-6 text-white/60">{note}</p>
    </article>
  )
}

function badgeClass(status: string) {
  const base = 'rounded-full border px-3 py-1 text-xs uppercase tracking-[0.2em]'
  if (status === 'Resolved') return `${base} border-aurora-mint/30 bg-aurora-mint/10 text-aurora-mint`
  if (status === 'Posted') return `${base} border-aurora-cyan/30 bg-aurora-cyan/10 text-aurora-cyan`
  return `${base} border-aurora-gold/30 bg-aurora-gold/10 text-aurora-gold`
}

function severityBar(severity: 'critical' | 'high' | 'medium' | 'low') {
  switch (severity) {
    case 'critical':
      return 'bg-aurora-coral'
    case 'high':
      return 'bg-aurora-gold'
    case 'medium':
      return 'bg-aurora-cyan'
    default:
      return 'bg-aurora-mint'
  }
}

export default App
