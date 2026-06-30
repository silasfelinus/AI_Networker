import { getActiveProjectSlugs, summarizeProject } from '../utils/repo'

export default defineEventHandler((event) => {
  try {
    const data = getActiveProjectSlugs().map((slug, index) => summarizeProject(slug, index + 1))
    return { success: true, data }
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unable to load projects'
    setResponseStatus(event, 500)
    return { success: false, message, statusCode: 500 }
  }
})
