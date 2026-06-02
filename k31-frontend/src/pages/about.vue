<template>
  <div :class="$style.page">
    <section :class="$style.hero">
      <p :class="$style.eyebrow">
        О проекте
      </p>
      <h1>Делаем первый шаг к заботе о здоровье понятнее</h1>
      <p>
        K+31 — учебный цифровой продукт для подбора пакетов медицинских услуг после короткого опроса. Мы хотим снизить порог входа: помочь человеку сориентироваться в вариантах и спокойно выбрать подходящий следующий шаг.
      </p>
    </section>

    <section :class="$style.contentGrid">
      <article>
        <span>01</span>
        <h2>Зачем нужен сервис</h2>
        <p>
          Каталоги медицинских услуг могут быть перегружены деталями. Пользователю трудно понять, какой набор анализов подойдет для планового контроля состояния или станет удобной точкой отсчета.
        </p>
      </article>
      <article>
        <span>02</span>
        <h2>Как устроен подход</h2>
        <p>
          Вместо самостоятельного поиска по длинному списку услуг человек отвечает на несколько вопросов и получает несколько подходящих пакетов с прозрачным составом и стоимостью.
        </p>
      </article>
      <article>
        <span>03</span>
        <h2>Границы продукта</h2>
        <p>
          Рекомендации не являются диагнозом и не заменяют прием врача. Это навигационный инструмент, который помогает сформулировать запрос и сделать выбор более осознанно.
        </p>
      </article>
    </section>

    <section :class="$style.hse">
      <div :class="$style.hseMark">
        HSE
      </div>
      <div>
        <p :class="$style.eyebrow">
          Образовательный контекст
        </p>
        <h2>Проект развивается в рамках учебной работы в НИУ ВШЭ</h2>
        <p>
          MVP создается как практический продуктовый и инженерный проект: мы проверяем гипотезы, проектируем пользовательский путь, развиваем интерфейс и серверную часть, а затем постепенно подключаем реальные данные.
        </p>
      </div>
    </section>

    <section :class="$style.cta">
      <div>
        <p :class="$style.eyebrow">
          Попробовать сценарий
        </p>
        <h2>Пройдите короткий опрос</h2>
        <p>Демо-версия работает на моковых данных и показывает основной пользовательский путь MVP.</p>
      </div>
      <NuxtLink to="/quiz">Начать опрос →</NuxtLink>
    </section>
  </div>
</template>

<style lang="scss" module>
.page {
  display: grid;
  max-width: 1192px;
  margin: 0 auto;
  gap: 56px;
}

.hero,
.hse,
.cta,
.contentGrid article {
  border: 1px solid #e1ebf6;
  border-radius: 22px;
  background: #fff;
}

.hero {
  padding: 62px;

  h1,
  p {
    max-width: 850px;
  }
}

.eyebrow {
  margin: 0 0 14px;
  color: #0877e8;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.hero h1,
.hse h2,
.cta h2 {
  margin: 0;
  color: #12315b;
  letter-spacing: -0.03em;
  line-height: 1.06;
}

.hero h1 {
  font-size: clamp(42px, 6vw, 68px);
}

.hero > p:not(.eyebrow),
.hse p:not(.eyebrow),
.cta p:not(.eyebrow) {
  margin: 20px 0 0;
  color: #66809f;
  font-size: 17px;
  line-height: 1.65;
}

.contentGrid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;

  article {
    padding: 28px;
  }

  span {
    color: #0877e8;
    font-size: 13px;
    font-weight: 700;
  }

  h2 {
    margin: 18px 0 0;
    color: #17446f;
    font-size: 22px;
  }

  p {
    margin: 12px 0 0;
    color: #738ba6;
    font-size: 14px;
    line-height: 1.65;
  }
}

.hse {
  display: grid;
  align-items: center;
  padding: 42px;
  background: linear-gradient(135deg, #fff, #edf6ff);
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 38px;

  h2 {
    max-width: 720px;
    font-size: clamp(30px, 4vw, 46px);
  }
}

.hseMark {
  display: grid;
  width: 190px;
  height: 190px;
  border-radius: 32px;
  background: #0877e8;
  box-shadow: 0 18px 40px rgb(8 119 232 / 24%);
  color: #fff;
  font-size: 52px;
  font-weight: 800;
  letter-spacing: -0.08em;
  place-items: center;
}

.cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 34px;
  gap: 24px;

  h2 {
    font-size: 32px;
  }

  a {
    flex: 0 0 auto;
    padding: 14px 20px;
    border-radius: 999px;
    background: #0877e8;
    color: #fff;
    font-size: 14px;
    font-weight: 700;
    text-decoration: none;
  }
}

@media (width <= 760px) {
  .page {
    gap: 36px;
  }

  .hero {
    padding: 30px 22px;
  }

  .contentGrid,
  .hse {
    grid-template-columns: 1fr;
  }

  .hse {
    padding: 28px 22px;
  }

  .hseMark {
    width: 96px;
    height: 96px;
    border-radius: 20px;
    font-size: 30px;
  }

  .cta {
    align-items: flex-start;
    flex-direction: column;
    padding: 24px;
  }
}
</style>
