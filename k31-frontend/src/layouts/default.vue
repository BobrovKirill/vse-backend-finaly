<script setup lang="ts">
import { ArrowRight, Lock } from '@element-plus/icons-vue'

const route = useRoute()

function isActive(path: string) {
  return route.path === path
}
</script>

<template>
  <el-container :class="$style.layout">
    <el-header :class="$style.header" height="72px">
      <div :class="$style.headerContent">
        <NuxtLink to="/" :class="$style.logo">
          <span :class="$style.logoMark">K<span>+31</span></span>
          <span :class="$style.logoText">
            БИОХАКИНГ<br>
            <strong>КОРОБКА</strong>
          </span>
        </NuxtLink>

        <nav :class="$style.navigation" aria-label="Основная навигация">
          <NuxtLink to="/" :class="{ [$style.active]: isActive('/') }">
            Главная
          </NuxtLink>
          <NuxtLink to="/about" :class="{ [$style.active]: isActive('/about') }">
            О проекте
          </NuxtLink>
          <NuxtLink to="/team" :class="{ [$style.active]: isActive('/team') }">
            Команда
          </NuxtLink>
        </nav>

        <div :class="$style.headerActions">
          <div :class="$style.protected">
            <el-icon :size="18">
              <Lock />
            </el-icon>
            <span>Данные защищены</span>
          </div>
          <NuxtLink to="/quiz" :class="$style.quizLink">
            Пройти опрос
            <el-icon><ArrowRight /></el-icon>
          </NuxtLink>
        </div>
      </div>
    </el-header>

    <el-main :class="$style.main">
      <slot />
    </el-main>

    <el-footer :class="$style.footer" height="auto">
      <div :class="$style.footerContent">
        <div>
          <NuxtLink to="/" :class="$style.footerLogo">
            K<span>+31</span>
          </NuxtLink>
          <p>Учебный сервис персонального подбора медицинских пакетов.</p>
        </div>

        <nav :class="$style.footerNavigation" aria-label="Навигация в подвале">
          <NuxtLink to="/">Главная</NuxtLink>
          <NuxtLink to="/about">О проекте</NuxtLink>
          <NuxtLink to="/team">Команда</NuxtLink>
          <NuxtLink to="/quiz">Пройти опрос</NuxtLink>
        </nav>
      </div>

      <div :class="$style.footerBottom">
        <span>© 2026 K+31</span>
        <span>Проект не заменяет медицинскую консультацию</span>
      </div>
    </el-footer>
  </el-container>
</template>

<style lang="scss" module>
.layout {
  min-height: 100vh;
  background: #f3f8fe;
}

.header {
  position: sticky;
  z-index: 10;
  top: 0;
  border-bottom: 1px solid #e1ebf6;
  backdrop-filter: blur(14px);
  background: rgb(255 255 255 / 88%);
}

.headerContent {
  display: flex;
  max-width: 1240px;
  height: 100%;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  margin: 0 auto;
  gap: 28px;
}

.logo {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  color: inherit;
  gap: 16px;
  text-decoration: none;
}

.logoMark,
.footerLogo {
  color: #075fcb;
  font-weight: 800;
  letter-spacing: -0.09em;

  span {
    color: #0b82ef;
  }
}

.logoMark {
  font-size: 31px;
}

.logoText {
  padding-left: 15px;
  border-left: 1px solid #d9e6f4;
  color: #65809e;
  font-size: 10px;
  letter-spacing: 0.08em;
  line-height: 1.35;

  strong {
    color: #345a80;
  }
}

.navigation,
.footerNavigation {
  display: flex;
  align-items: center;

  a {
    color: #5c7895;
    font-size: 14px;
    text-decoration: none;
    transition: color 160ms ease;

    &:hover,
    &.active {
      color: #0877e8;
    }
  }
}

.navigation {
  margin-left: auto;
  gap: 22px;
}

.headerActions,
.protected,
.quizLink {
  display: flex;
  align-items: center;
}

.headerActions {
  gap: 18px;
}

.protected {
  color: #6d87a4;
  font-size: 12px;
  gap: 7px;

  :global(.el-icon) {
    color: #0b82ef;
  }
}

.quizLink {
  padding: 10px 15px;
  border-radius: 999px;
  background: #0877e8;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  gap: 5px;
  text-decoration: none;
  transition: background 160ms ease;

  &:hover {
    background: #0568ce;
  }
}

.main {
  width: 100%;
  padding: 30px 24px 64px;
}

.footer {
  padding: 42px 24px 20px;
  border-top: 1px solid #deebf7;
  background: #eaf3fc;
}

.footerContent,
.footerBottom {
  display: flex;
  max-width: 1192px;
  justify-content: space-between;
  margin: 0 auto;
  gap: 28px;
}

.footerLogo {
  font-size: 28px;
  text-decoration: none;
}

.footerContent p {
  max-width: 380px;
  margin: 14px 0 0;
  color: #6d87a4;
  font-size: 14px;
  line-height: 1.55;
}

.footerNavigation {
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 18px;
}

.footerBottom {
  padding-top: 18px;
  border-top: 1px solid #d6e5f4;
  margin-top: 32px;
  color: #8298b0;
  font-size: 12px;
}

@media (width <= 960px) {
  .protected {
    display: none;
  }
}

@media (width <= 760px) {
  .header {
    height: auto !important;
  }

  .headerContent {
    min-height: 72px;
    flex-wrap: wrap;
    padding: 12px 16px;
    gap: 10px 16px;
  }

  .logoText {
    display: none;
  }

  .navigation {
    order: 3;
    width: 100%;
    justify-content: space-between;
    margin: 0;
    gap: 12px;
  }

  .quizLink {
    padding: 9px 12px;
    font-size: 12px;
  }

  .main {
    padding: 16px 12px 42px;
  }

  .footer {
    padding: 32px 18px 18px;
  }

  .footerContent,
  .footerBottom {
    flex-direction: column;
    gap: 18px;
  }

  .footerNavigation {
    align-items: flex-start;
    flex-direction: column;
    gap: 12px;
  }
}
</style>
