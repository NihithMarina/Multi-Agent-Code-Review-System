export type HealthResponse = {
  message: string
}

export type AnalyticsOverview = {
  total_reviews: number
  open_reviews: number
  findings_by_severity: Record<string, number>
}

export type Finding = {
  agent: string
  severity: string
  title: string
  explanation: string
  suggestion?: string | null
  file_path?: string | null
}

export type ReviewSummary = {
  id: number
  repository_id: number
  pull_request_number: number
  commit_sha: string
  status: string
  summary?: string | null
  findings?: Finding[]
  created_at: string
}
