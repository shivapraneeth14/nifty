import { post } from './client'

export function submitFeedback(data: {
  brief_id: string
  article_id?: string
  helpful: boolean
}) {
  return post('/feedback', data)
}
