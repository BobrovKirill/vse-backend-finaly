import type { QuizPackage, QuizQuestion } from '~/types/quiz'

export type QuizStage = 'intro' | 'questions' | 'contacts' | 'results'

export interface QuizFlowProps {
  showIntro?: boolean
}

export function getRecommendedPackages(
  questions: QuizQuestion[],
  packages: QuizPackage[],
  selectedAnswers: Record<number, number>,
): QuizPackage[] {
  const scores = new Map(packages.map(item => [item.code, 0]))

  for (const question of questions) {
    const selectedAnswerId = selectedAnswers[question.id]
    const selectedAnswer = question.answers.find(answer => answer.id === selectedAnswerId)

    if (!selectedAnswer)
      continue

    for (const [packageCode, weight] of Object.entries(selectedAnswer.recommendationWeights))
      scores.set(packageCode, (scores.get(packageCode) ?? 0) + weight)
  }

  return [...packages]
    .sort((first, second) => (scores.get(second.code) ?? 0) - (scores.get(first.code) ?? 0))
    .slice(0, 2)
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat('ru-RU').format(price)
}
