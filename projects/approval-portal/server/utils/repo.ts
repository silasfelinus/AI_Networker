import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { basename, join, resolve } from 'node:path'
import YAML from 'yaml'

type ProjectOverride = {
  slug: string
  status: string
  priority?: string
  kind?: string
}

type RoadmapMilestone = {
  id: string
  title: string
  weight?: number
  status?: string
}

type RoadmapTask = {
  id: string
  title: string
  milestone?: string
  status: string
  owner?: string | null
  updated?: string
  passes?: number
  stakes?: string
  depends_on?: string | string[]
  gate_human?: boolean
  approved_by_human?: boolean
  note?: string
}

type Roadmap = {
  project: string
  kind: string
  notes_from_silas?: string
  milestones?: RoadmapMilestone[]
  tasks?: RoadmapTask[]
}

const repoRoot = resolve(process.cwd(), '../..')

const readText = (path: string) => readFileSync(join(repoRoot, path), 'utf8')
const readYaml = <T>(path: string) => YAML.parse(readText(path)) as T

const countByStatus = (items: Array<{ status?: string }>) => items.reduce<Record<string, number>>((counts, item) => {
  const status = item.status ?? 'unknown'
  counts[status] = (counts[status] ?? 0) + 1
  return counts
}, {})

const progressPercent = (milestones: RoadmapMilestone[]) => {
  const total = milestones.reduce((sum, milestone) => sum + (milestone.weight ?? 0), 0)
  if (!total) return 0
  const done = milestones.reduce((sum, milestone) => {
    if (milestone.status === 'done') return sum + (milestone.weight ?? 0)
    if (milestone.status === 'in-progress') return sum + (milestone.weight ?? 0) / 2
    return sum
  }, 0)
  return Math.round((done / total) * 100)
}

const latestUpdatedTask = (tasks: RoadmapTask[]) => tasks
  .filter((task) => task.updated)
  .sort((a, b) => new Date(b.updated ?? '').getTime() - new Date(a.updated ?? '').getTime())[0] ?? null

export const getPriorityOrder = () => readYaml<{ order?: string[] }>('projects/priority.yaml').order ?? []
export const getOverrides = () => readYaml<{ overrides?: ProjectOverride[] }>('project-overrides.yaml').overrides ?? []
export const readRoadmap = (slug: string) => readYaml<Roadmap>(`projects/${slug}/roadmap.yaml`)

export const getActiveProjectSlugs = () => {
  const overrides = new Map(getOverrides().map((override) => [override.slug, override]))
  return getPriorityOrder().filter((slug) => overrides.get(slug)?.status === 'active')
}

export const summarizeProject = (slug: string, priorityRank: number) => {
  const override = getOverrides().find((item) => item.slug === slug)
  const roadmap = readRoadmap(slug)
  const milestones = roadmap.milestones ?? []
  const tasks = roadmap.tasks ?? []
  const taskCounts = countByStatus(tasks)

  return {
    slug,
    kind: override?.kind ?? roadmap.kind,
    overrideStatus: override?.status ?? 'unknown',
    priority: override?.priority ?? 'normal',
    priorityRank,
    progressPercent: progressPercent(milestones),
    milestoneCounts: countByStatus(milestones),
    taskCounts,
    readyTaskCount: taskCounts.ready ?? 0,
    needsHumanCount: taskCounts['needs-human'] ?? 0,
    reviewCount: taskCounts.review ?? 0,
    latestUpdatedTask: latestUpdatedTask(tasks),
  }
}

export const extractControlBlock = (slug: string) => {
  const controlPath = join(repoRoot, 'CONTROL.md')
  if (!existsSync(controlPath)) return ''
  const control = readFileSync(controlPath, 'utf8')
  const start = control.indexOf(`### ${slug}`)
  if (start === -1) return ''
  const rest = control.slice(start)
  const next = rest.indexOf('\n### ', 1)
  return (next === -1 ? rest : rest.slice(0, next)).trim()
}

export const listPitches = () => {
  const pitchesPath = join(repoRoot, 'pitches')
  if (!existsSync(pitchesPath)) return []

  return readdirSync(pitchesPath).filter((file) => file.endsWith('.md')).map((file) => {
    const content = readFileSync(join(pitchesPath, file), 'utf8')
    const lines = content.split('\n')
    const readValue = (key: string) => lines.find((line) => line.startsWith(`${key}:`))?.replace(`${key}:`, '').trim() ?? ''
    const bodyStart = lines.findIndex((line) => line.trim() === '## The idea')
    const body = bodyStart === -1 ? content : lines.slice(bodyStart + 1).join('\n').trim()

    return {
      slug: basename(file, '.md'),
      title: lines.find((line) => line.startsWith('# Pitch:'))?.replace('# Pitch:', '').trim() ?? basename(file, '.md'),
      date: readValue('date'),
      projectTarget: readValue('project-target'),
      status: readValue('status') || 'unknown',
      excerpt: body.slice(0, 360),
    }
  }).sort((a, b) => b.date.localeCompare(a.date))
}
