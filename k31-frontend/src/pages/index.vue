<script setup lang="ts">
const selectedAnswer = ref('poor-sleep')

const options = [
  {
    value: 'good-sleep',
    icon: '😴',
    title: 'Сплю хорошо, высыпаюсь',
    description: 'Просыпаюсь отдохнувшим и полным сил'
  },
  {
    value: 'sometimes-difficult',
    icon: '😐',
    title: 'Бывают трудности',
    description: 'Иногда долго засыпаю или просыпаюсь ночью'
  },
  {
    value: 'poor-sleep',
    icon: '😣',
    title: 'Сплю плохо',
    description: 'Часто просыпаюсь, утро начинается с усталости'
  },
  {
    value: 'very-poor',
    icon: '😫',
    title: 'Очень плохо',
    description: 'Проблемы со сном почти каждый день'
  }
]
</script>

<template>
  <div :class="$style.page">
    <!-- Quiz Container -->
    <div :class="$style.quizContainer">
      <!-- Category -->
      <div :class="$style.category">
        <el-tag type="info" size="large" effect="light">
          <span>🌙</span> СОН И ЭНЕРГИЯ
        </el-tag>
      </div>

      <!-- Question -->
      <h1 :class="$style.question">
        Как вы обычно спите?
      </h1>
      <p :class="$style.subtitle">
        Это поможет нам подобрать добавки и практики<br>
        для улучшения качества сна и восстановления.
      </p>

      <!-- Options -->
      <el-radio-group v-model="selectedAnswer" :class="$style.options">
        <el-card
            v-for="(option, index) in options"
            :key="index"
            :class="[$style.optionCard, { [$style.selected]: selectedAnswer === option.value }]"
            shadow="hover"
        >
          <el-radio :label="option.value" :class="$style.radio">
            <div :class="$style.optionContent">
              <div :class="$style.icon">{{ option.icon }}</div>
              <div :class="$style.text">
                <div :class="$style.title">{{ option.title }}</div>
                <div :class="$style.description">{{ option.description }}</div>
              </div>
            </div>
          </el-radio>
        </el-card>
      </el-radio-group>

      <!-- Disclaimer -->
      <div :class="$style.disclaimer">
        <span>✨</span>
        <p>Мы не ставим диагнозы.<br>Ваши ответы помогут подобрать персональные рекомендации и состав следующей биохакинг-коробки.</p>
      </div>

      <!-- Navigation -->
      <div :class="$style.navigation">
        <el-button
            :class="$style.backBtn"
            size="large"
        >
          ← Назад
        </el-button>

        <el-button
            type="primary"
            size="large"
            :class="$style.nextBtn"
        >
          Далее →
        </el-button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" module>
.page {
  display: flex;
  justify-content: center;
}

.quizContainer {
  max-width: 720px;
  width: 100%;
}

.category {
  margin-bottom: 24px;
}

.question {
  font-size: 32px;
  font-weight: 700;
  color: #1e3a8a;
  margin-bottom: 12px;
  line-height: 1.2;
}

.subtitle {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 40px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.optionCard {
  transition: all 0.2s;
  cursor: pointer;
  border: 2px solid transparent;

  &.selected {
    border-color: #3b82f6;
    background-color: #f0f9ff;
  }
}

.optionContent {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 8px 0;
}

.icon {
  font-size: 28px;
  margin-top: 2px;
}

.text {
  flex: 1;
}

.title {
  font-weight: 600;
  font-size: 17px;
  color: #1e2937;
  margin-bottom: 4px;
}

.description {
  font-size: 15px;
  color: #64748b;
  line-height: 1.4;
}

.radio {
  width: 100%;
}

.disclaimer {
  background-color: #f0f9ff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
  font-size: 14px;
  color: #475569;

  p {
    margin: 0;
    line-height: 1.5;
  }
}

.navigation {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.backBtn {
  padding: 0 32px;
}

.nextBtn {
  padding: 0 48px;
}
</style>