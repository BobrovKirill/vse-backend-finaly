<script setup lang="ts">
import { Lock } from '@element-plus/icons-vue'
const route = useRoute()

// Для квиза показываем прогресс
const showProgress = computed(() => route.path === '/' || route.path.includes('quiz'))

const currentStep = ref(3)   // пока хардкод, потом сделаем динамику
const totalSteps = ref(8)
const progress = computed(() => Math.round((currentStep.value / totalSteps.value) * 100))
</script>

<template>
  <el-container :class="$style.layout">
    <!-- Header -->
    <el-header :class="$style.header" height="70px">
      <div :class="$style.headerContent">
        <!-- Logo -->
        <div :class="$style.logo">
          <span class="text-3xl font-bold text-[#1e40af]">K</span>
          <span class="text-3xl font-bold text-[#3b82f6]">+31</span>
          <div :class="$style.logoText">
            БИОХАКИНГ<br>
            <span>КОРОБКА</span>
          </div>
        </div>

        <!-- Progress -->
        <div v-if="showProgress" :class="$style.progressContainer">
          <span :class="$style.progressText">
            Шаг {{ currentStep }} из {{ totalSteps }}
          </span>

          <el-progress
              :percentage="progress"
              :stroke-width="6"
              style="width: 360px;"
              class="w-64"
          />

          <span :class="$style.progressPercent">{{ progress }}%</span>
        </div>

        <!-- Right side -->
        <div :class="$style.rightSection">
          <span :class="$style.protectedText">Ваши данные защищены</span>
          <el-icon :size="22" color="#3b82f6">
            <Lock />
          </el-icon>
        </div>
      </div>
    </el-header>

    <!-- Main Content -->
    <el-main :class="$style.main">
      <slot />
    </el-main>
  </el-container>
</template>

<style lang="scss" module>
.layout {
  min-height: 100vh;
  background-color: #f8fafc;
}

.header {
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.headerContent {
  height: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logoText {
  font-size: 13px;
  line-height: 1.1;
  color: #6b7280;

  span {
    font-weight: 500;
    color: #374151;
  }
}

.progressContainer {
  display: flex;
  align-items: center;
  gap: 16px;
}

.progressText {
  font-size: 14px;
  color: #6b7280;
  white-space: nowrap;
}

.progressPercent {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.rightSection {
  display: flex;
  align-items: center;
  gap: 12px;
}

.protectedText {
  font-size: 14px;
  color: #6b7280;
  display: none;

  @media (min-width: 640px) {
    display: block;
  }
}

.main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
  background-color: #f8fafc;
}
</style>