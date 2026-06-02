export type QuizQuestionType = 'single' | 'multiple'

export interface QuizAnswer {
  id: number
  questionId: number
  text: string
  description: string
  icon: string
  recommendationWeights: Record<string, number>
}

export interface QuizQuestion {
  id: number
  text: string
  helpText: string
  type: QuizQuestionType
  answers: QuizAnswer[]
}

export interface PackageService {
  id: number
  title: string
  description?: string
}

export interface QuizPackage {
  id: number
  code: string
  title: string
  description: string
  price: number
  services: PackageService[]
  checkoutUrl: string
  isPopular?: boolean
}
