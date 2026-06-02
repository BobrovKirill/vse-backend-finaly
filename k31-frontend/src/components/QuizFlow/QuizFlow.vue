<script setup lang="ts">
import type { QuizFlowProps, QuizStage } from '.'
import { ArrowLeft, ArrowRight, Check, Lock, Phone, User } from '@element-plus/icons-vue'
import { quizPackages, quizQuestions } from '~/mocs/quiz'
import { formatPrice, getRecommendedPackages } from '.'

const props = withDefaults(defineProps<QuizFlowProps>(), {
  showIntro: false,
})

const stage = ref<QuizStage>(props.showIntro ? 'intro' : 'questions')
const currentQuestionIndex = ref(0)
const selectedAnswers = ref<Record<number, number>>({})
const contact = reactive({
  name: '',
  phone: '',
})

const activeQuestion = computed(() => quizQuestions[currentQuestionIndex.value])
const selectedAnswer = computed({
  get: () => selectedAnswers.value[activeQuestion.value.id],
  set: (answerId: number) => {
    selectedAnswers.value[activeQuestion.value.id] = answerId
  },
})
const isFirstQuestion = computed(() => currentQuestionIndex.value === 0)
const isLastQuestion = computed(() => currentQuestionIndex.value === quizQuestions.length - 1)
const progress = computed(() => Math.round(((currentQuestionIndex.value + 1) / quizQuestions.length) * 100))
const recommendedPackages = computed(() => getRecommendedPackages(quizQuestions, quizPackages, selectedAnswers.value))

function startQuiz() {
  stage.value = 'questions'
}

function goNext() {
  if (!selectedAnswer.value)
    return

  if (isLastQuestion.value) {
    stage.value = 'contacts'
    return
  }

  currentQuestionIndex.value += 1
}

async function goBack() {
  if (!isFirstQuestion.value) {
    currentQuestionIndex.value -= 1
    return
  }

  if (props.showIntro) {
    stage.value = 'intro'
    return
  }

  await navigateTo('/')
}

function showResults() {
  stage.value = 'results'
}

function restartQuiz() {
  selectedAnswers.value = {}
  contact.name = ''
  contact.phone = ''
  currentQuestionIndex.value = 0
  stage.value = props.showIntro ? 'intro' : 'questions'
}
</script>

<template>
  <section :class="$style.quizShell">
    <div v-if="stage === 'intro'" :class="$style.intro">
      <div :class="$style.introContent">
        <p :class="$style.eyebrow">
          Персональный подбор
        </p>
        <h1 :class="$style.introTitle">
          Найдите подходящий пакет заботы о здоровье
        </h1>
        <p :class="$style.introText">
          Ответьте на несколько вопросов о самочувствии. Мы предложим подходящие варианты обследований без диагнозов и сложных терминов.
        </p>
        <div :class="$style.introMeta">
          <span><el-icon><Check /></el-icon> 4 коротких вопроса</span>
          <span><el-icon><Lock /></el-icon> Ответы защищены</span>
        </div>
        <el-button type="primary" size="large" round :class="$style.primaryButton" @click="startQuiz">
          Начать опрос
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>

      <div :class="$style.illustration" aria-hidden="true">
        <div :class="$style.illustrationGlow" />
        <div :class="$style.illustrationCard">
          <span :class="$style.illustrationIcon">+</span>
          <strong>Персональный план</strong>
          <small>анализы и процедуры</small>
        </div>
        <div :class="$style.illustrationBubble">
          <Check />
        </div>
      </div>
    </div>

    <div v-else-if="stage === 'questions'" :class="$style.questionLayout">
      <div :class="$style.questionPanel">
        <div :class="$style.progressHeader">
          <span>Шаг {{ currentQuestionIndex + 1 }} из {{ quizQuestions.length }}</span>
          <strong>{{ progress }}%</strong>
        </div>
        <el-progress :percentage="progress" :stroke-width="7" :show-text="false" />

        <div :class="$style.questionCopy">
          <h1>{{ activeQuestion.text }}</h1>
          <p :class="$style.questionHelp">
            {{ activeQuestion.helpText }}
          </p>
        </div>

        <el-radio-group v-model="selectedAnswer" :class="$style.options">
          <label
            v-for="answer in activeQuestion.answers"
            :key="answer.id"
            :class="[$style.optionCard, { [$style.selected]: selectedAnswer === answer.id }]"
          >
            <span :class="$style.optionIcon">{{ answer.icon }}</span>
            <span :class="$style.optionText">
              <strong>{{ answer.text }}</strong>
              <small>{{ answer.description }}</small>
            </span>
            <el-radio :value="answer.id" :class="$style.radio" />
          </label>
        </el-radio-group>

        <div :class="$style.disclaimer">
          <span :class="$style.spark">✦</span>
          <p :class="$style.disclaimerText">
            <strong>Мы не ставим диагнозы.</strong><br>Ответы используются только для подбора персональных рекомендаций.
          </p>
        </div>

        <div :class="$style.navigation">
          <el-button size="large" round @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            Назад
          </el-button>
          <el-button type="primary" size="large" round :disabled="!selectedAnswer" @click="goNext">
            {{ isLastQuestion ? 'Завершить' : 'Далее' }}
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>

      <div :class="$style.sideIllustration" aria-hidden="true">
        <div :class="$style.sideCircle" />
        <div :class="$style.sideCard">
          <span>✦</span>
          <strong>Ваши ответы</strong>
          <small>помогут собрать персональную рекомендацию</small>
        </div>
      </div>
    </div>

    <div v-else-if="stage === 'contacts'" :class="$style.contacts">
      <p :class="$style.eyebrow">
        Почти готово
      </p>
      <h1>Куда отправить рекомендации?</h1>
      <p :class="$style.contactsLead">
        Оставьте контакты, чтобы сохранить результат. Для демо этот шаг можно пропустить.
      </p>

      <el-form :model="contact" :class="$style.contactForm" label-position="top">
        <el-form-item label="Ваше имя">
          <el-input v-model="contact.name" size="large" placeholder="Например, Алексей" :prefix-icon="User" />
        </el-form-item>
        <el-form-item label="Телефон">
          <el-input v-model="contact.phone" size="large" placeholder="+7 999 000-00-00" :prefix-icon="Phone" />
        </el-form-item>
      </el-form>

      <div :class="$style.navigation">
        <el-button size="large" round @click="stage = 'questions'">
          <el-icon><ArrowLeft /></el-icon>
          Назад
        </el-button>
        <el-button type="primary" size="large" round @click="showResults">
          Показать результат
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
    </div>

    <div v-else :class="$style.results">
      <p :class="$style.eyebrow">
        Персональная рекомендация
      </p>
      <h1>Подобрали подходящие варианты</h1>
      <p :class="$style.resultsLead">
        Это не медицинское заключение. Перед прохождением процедур при необходимости проконсультируйтесь со специалистом.
      </p>

      <div :class="$style.packageGrid">
        <article v-for="item in recommendedPackages" :key="item.id" :class="$style.packageCard">
          <div :class="$style.packageHeader">
            <span v-if="item.isPopular" :class="$style.popular">Популярный выбор</span>
            <h2>{{ item.title }}</h2>
            <p :class="$style.packageDescription">
              {{ item.description }}
            </p>
          </div>
          <ul>
            <li v-for="service in item.services" :key="service.id">
              <el-icon><Check /></el-icon>
              {{ service.title }}
            </li>
          </ul>
          <div :class="$style.packageFooter">
            <div>
              <small>Стоимость пакета</small>
              <strong>{{ formatPrice(item.price) }} ₽</strong>
            </div>
            <el-button tag="a" :href="item.checkoutUrl" target="_blank" type="primary" round>
              Оформить
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </article>
      </div>

      <el-button text :class="$style.restart" @click="restartQuiz">
        Пройти опрос заново
      </el-button>
    </div>
  </section>
</template>

<style lang="scss" module>
.quizShell {
  width: min(100%, 1120px);
  margin: 0 auto;
}

.intro,
.questionLayout {
  display: grid;
  overflow: hidden;
  min-height: 680px;
  border: 1px solid #e4edf9;
  border-radius: 28px;
  background: #fff;
  box-shadow: 0 22px 70px rgb(36 87 145 / 12%);
}

.intro {
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
}

.introContent {
  align-self: center;
  padding: 72px;
}

.eyebrow {
  margin: 0 0 14px;
  color: #0877e8;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.introTitle,
.contacts h1,
.results h1 {
  margin: 0;
  color: #12315b;
  font-size: clamp(36px, 5vw, 58px);
  line-height: 1.06;
}

.introText,
.contactsLead,
.resultsLead {
  max-width: 680px;
  margin: 24px 0 0;
  color: #66809f;
  font-size: 17px;
  line-height: 1.65;
}

.introMeta {
  display: flex;
  flex-wrap: wrap;
  margin: 30px 0;
  color: #54708f;
  font-size: 14px;
  gap: 18px;

  span {
    display: flex;
    align-items: center;
    gap: 7px;
  }

  :global(.el-icon) {
    color: #1680ed;
  }
}

.primaryButton {
  min-width: 190px;
  height: 52px;
  font-weight: 700;
}

.illustration,
.sideIllustration {
  position: relative;
  overflow: hidden;
  background: linear-gradient(145deg, #eaf4ff 0%, #f8fbff 100%);
}

.illustrationGlow,
.sideCircle {
  position: absolute;
  width: 390px;
  height: 390px;
  border-radius: 50%;
  background: linear-gradient(145deg, #c4e0ff, #eef7ff);
}

.illustrationGlow {
  top: 98px;
  right: -55px;
}

.illustrationCard,
.sideCard {
  position: absolute;
  display: flex;
  flex-direction: column;
  padding: 28px;
  border: 1px solid rgb(255 255 255 / 70%);
  border-radius: 22px;
  backdrop-filter: blur(12px);
  background: rgb(255 255 255 / 78%);
  box-shadow: 0 20px 55px rgb(47 112 183 / 18%);
  color: #174a82;
  gap: 8px;
}

.illustrationCard {
  top: 230px;
  right: 60px;
  left: 52px;
}

.illustrationIcon {
  color: #0877e8;
  font-size: 64px;
  font-weight: 300;
  line-height: 0.8;
}

.illustrationBubble {
  position: absolute;
  top: 170px;
  right: 40px;
  display: grid;
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: #0877e8;
  box-shadow: 0 14px 28px rgb(8 119 232 / 28%);
  color: #fff;
  place-items: center;

  svg {
    width: 32px;
  }
}

.questionLayout {
  grid-template-columns: minmax(0, 1fr) 310px;
}

.questionPanel {
  padding: 46px 52px;
}

.progressHeader {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #6e87a5;
  font-size: 14px;

  strong {
    color: #0877e8;
  }
}

.questionCopy {
  margin: 44px 0 30px;

  h1 {
    max-width: 680px;
    margin: 0;
    color: #12315b;
    font-size: clamp(30px, 4vw, 42px);
    line-height: 1.14;
  }
}

.questionHelp {
  max-width: 620px;
  margin: 15px 0 0;
  color: #6c84a1;
  font-size: 16px;
  line-height: 1.55;
}

.options {
  display: grid;
  gap: 12px;
}

.optionCard {
  display: flex;
  min-height: 82px;
  align-items: center;
  padding: 14px 18px;
  border: 1px solid #dce7f4;
  border-radius: 14px;
  background: #fff;
  cursor: pointer;
  gap: 16px;
  transition: 180ms ease;

  &:hover,
  &.selected {
    border-color: #1680ed;
    background: #f5faff;
    box-shadow: 0 7px 18px rgb(8 119 232 / 8%);
  }
}

.optionIcon {
  display: grid;
  width: 48px;
  height: 48px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: #edf6ff;
  color: #0877e8;
  font-size: 25px;
  place-items: center;
}

.optionText {
  display: flex;
  min-width: 0;
  flex: 1;
  flex-direction: column;
  color: #24476f;
  gap: 5px;

  strong {
    font-size: 15px;
  }

  small {
    color: #738ba6;
    font-size: 13px;
  }
}

.radio {
  margin-right: 0;

  :global(.el-radio__label) {
    display: none;
  }
}

.disclaimer {
  display: flex;
  padding: 16px 18px;
  border-radius: 12px;
  margin-top: 22px;
  background: #eef6ff;
  color: #557493;
  font-size: 13px;
  gap: 12px;

  strong {
    color: #0877e8;
  }
}

.spark {
  color: #0877e8;
  font-size: 24px;
}

.disclaimerText {
  margin: 0;
  line-height: 1.5;
}

.navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
  gap: 14px;

  :global(.el-button) {
    min-width: 132px;
    height: 46px;
  }
}

.sideCircle {
  top: 110px;
  right: -148px;
}

.sideCard {
  right: 24px;
  bottom: 64px;
  left: 24px;

  span {
    color: #0877e8;
    font-size: 36px;
  }

  small {
    color: #6c84a1;
    line-height: 1.45;
  }
}

.contacts,
.results {
  padding: 58px;
  border: 1px solid #e4edf9;
  border-radius: 28px;
  background: #fff;
  box-shadow: 0 22px 70px rgb(36 87 145 / 12%);
}

.contacts {
  max-width: 680px;
  margin: 0 auto;
}

.contacts h1,
.results h1 {
  font-size: clamp(32px, 4vw, 48px);
}

.contactForm {
  margin-top: 30px;
}

.results {
  text-align: center;
}

.resultsLead {
  margin-right: auto;
  margin-left: auto;
}

.packageGrid {
  display: grid;
  margin-top: 36px;
  gap: 18px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  text-align: left;
}

.packageCard {
  display: flex;
  flex-direction: column;
  padding: 26px;
  border: 1px solid #dfeaf7;
  border-radius: 18px;
  background: #fff;

  ul {
    display: grid;
    padding: 0;
    margin: 22px 0 26px;
    gap: 11px;
    list-style: none;
  }

  li {
    display: flex;
    align-items: flex-start;
    color: #557493;
    font-size: 14px;
    gap: 8px;
    line-height: 1.4;
  }

  :global(.el-icon) {
    flex: 0 0 auto;
    margin-top: 2px;
    color: #1680ed;
  }
}

.packageHeader {
  flex: 1;

  h2 {
    margin: 8px 0 0;
    color: #17446f;
    font-size: 23px;
  }
}

.packageDescription {
  margin: 12px 0 0;
  color: #738ba6;
  font-size: 14px;
  line-height: 1.55;
}

.popular {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 999px;
  background: #eaf5ff;
  color: #0877e8;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.packageFooter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18px;
  border-top: 1px solid #edf2f8;
  gap: 12px;

  div {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  small {
    color: #86a0ba;
    font-size: 12px;
  }

  strong {
    color: #17446f;
    font-size: 22px;
  }
}

.restart {
  margin-top: 24px;
}

@media (width <= 900px) {
  .intro,
  .questionLayout {
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .introContent,
  .questionPanel {
    padding: 38px 30px;
  }

  .illustration,
  .sideIllustration {
    display: none;
  }
}

@media (width <= 640px) {
  .introContent,
  .questionPanel,
  .contacts,
  .results {
    padding: 25px 18px;
  }

  .intro,
  .questionLayout,
  .contacts,
  .results {
    border-radius: 18px;
  }

  .questionCopy {
    margin: 32px 0 24px;
  }

  .optionCard {
    min-height: 76px;
    padding: 12px;
    gap: 11px;
  }

  .optionIcon {
    width: 42px;
    height: 42px;
    font-size: 22px;
  }

  .navigation {
    :global(.el-button) {
      min-width: 0;
      flex: 1;
    }
  }

  .packageGrid {
    grid-template-columns: 1fr;
  }

  .packageFooter {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
