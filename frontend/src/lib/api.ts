import type { AnalyticsOverview, HealthResponse, ReviewSummary } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  return response.json() as Promise<T>
}

export function getHealth() {
  return request<HealthResponse>('/api/v1/health')
}

export function getAnalytics() {
  return request<AnalyticsOverview>('/api/v1/analytics/overview')
}

export function getReview(reviewId: number) {
  return request<ReviewSummary>(`/api/v1/reviews/${reviewId}`)
}
