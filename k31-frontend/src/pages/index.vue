<template>
  <div :class="$style.page">
    <section :class="$style.hero">
      <div>
        <p :class="$style.eyebrow">
          Забота о здоровье понятным языком
        </p>
        <h1>Персональный маршрут к полезным обследованиям</h1>
        <p :class="$style.heroText">
          K+31 помогает выбрать подходящий набор анализов и процедур после короткого опроса о самочувствии. Без сложных терминов, самостоятельных диагнозов и лишних шагов.
        </p>
        <div :class="$style.heroActions">
          <a href="#quiz" :class="$style.primaryLink">Подобрать пакет</a>
          <NuxtLink to="/about" :class="$style.secondaryLink">Узнать о проекте</NuxtLink>
        </div>
      </div>

      <div :class="$style.heroVisual" aria-hidden="true">
        <span :class="$style.heroCircle" />
        <span :class="$style.heroCross">+</span>
        <div :class="$style.heroCard">
          <strong>Короткий опрос</strong>
          <span>Понятные рекомендации</span>
        </div>
        <div :class="$style.heroCardSecondary">
          <strong>4 вопроса</strong>
          <span>для первого подбора</span>
        </div>
      </div>
    </section>

    <section :class="$style.section">
      <div :class="$style.sectionHeading">
        <p :class="$style.eyebrow">
          О сервисе
        </p>
        <h2>Помогаем начать с понятного следующего шага</h2>
        <p>
          Когда вариантов обследований много, бывает сложно понять, с чего начать. Наш сервис собирает исходную информацию и предлагает несколько подходящих пакетов услуг, составленных вокруг распространенных запросов.
        </p>
      </div>

      <div :class="$style.featureGrid">
        <article>
          <span>01</span>
          <h3>Небольшой опрос</h3>
          <p>Отвечаете на несколько вопросов о сне, уровне энергии, стрессе и регулярности обследований.</p>
        </article>
        <article>
          <span>02</span>
          <h3>Персональный подбор</h3>
          <p>Получаете несколько пакетов с понятным составом: анализами, процедурами и итоговой стоимостью.</p>
        </article>
        <article>
          <span>03</span>
          <h3>Осознанное решение</h3>
          <p>Выбираете подходящий вариант и переходите к оформлению на внешнем ресурсе клиники.</p>
        </article>
      </div>
    </section>

    <section :class="$style.note">
      <strong>Важно помнить</strong>
      <p>
        Сервис не ставит диагнозы и не заменяет консультацию врача. Его задача — помочь сориентироваться в доступных вариантах и сделать первый шаг проще.
      </p>
    </section>

    <section id="quiz" :class="$style.quizSection">
      <div :class="$style.sectionHeading">
        <p :class="$style.eyebrow">
          Начать подбор
        </p>
        <h2>Ответьте на несколько вопросов</h2>
        <p>На главной странице опрос начинается со стартового окна. Для партнерских ссылок доступна отдельная страница с немедленным началом.</p>
      </div>

      <QuizFlow show-intro />
    </section>

    <section :class="[$style.section, $style.aboutPreview]">
      <div>
        <p :class="$style.eyebrow">
          Учебный проект
        </p>
        <h2>Развиваем продукт в образовательном контексте НИУ ВШЭ</h2>
      </div>
      <div>
        <p>
          Мы исследуем, как цифровые сервисы могут сделать знакомство с медицинскими услугами более понятным и спокойным. MVP помогает проверить основной сценарий: от короткой анкеты до выбора подходящего пакета.
        </p>
        <NuxtLink to="/about" :class="$style.textLink">Подробнее о проекте →</NuxtLink>
      </div>
    </section>
  </div>
</template>

<style lang="scss" module>
.page {
  display: grid;
  max-width: 1192px;
  margin: 0 auto;
  gap: 84px;
}

.hero {
  display: grid;
  min-height: 590px;
  overflow: hidden;
  border: 1px solid #e4edf9;
  border-radius: 28px;
  background: #fff;
  box-shadow: 0 22px 70px rgb(36 87 145 / 12%);
  grid-template-columns: minmax(0, 1.12fr) minmax(350px, 0.88fr);

  > div:first-child {
    align-self: center;
    padding: 62px;
  }

  h1 {
    max-width: 690px;
    margin: 0;
    color: #12315b;
    font-size: clamp(42px, 5vw, 68px);
    letter-spacing: -0.04em;
    line-height: 1.02;
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

.heroText,
.sectionHeading > p:not(.eyebrow),
.aboutPreview p {
  color: #66809f;
  font-size: 17px;
  line-height: 1.65;
}

.heroText {
  max-width: 690px;
  margin: 24px 0 0;
}

.heroActions {
  display: flex;
  flex-wrap: wrap;
  margin-top: 32px;
  gap: 12px;
}

.primaryLink,
.secondaryLink {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 22px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
}

.primaryLink {
  background: #0877e8;
  color: #fff;
}

.secondaryLink {
  border: 1px solid #d3e2f1;
  color: #477091;
}

.heroVisual {
  position: relative;
  overflow: hidden;
  background: linear-gradient(145deg, #e9f4ff, #f9fcff);
}

.heroCircle {
  position: absolute;
  top: 106px;
  right: -35px;
  width: 390px;
  height: 390px;
  border-radius: 50%;
  background: linear-gradient(145deg, #bedcff, #edf7ff);
}

.heroCross {
  position: absolute;
  top: 142px;
  right: 58px;
  color: #0877e8;
  font-size: 82px;
  font-weight: 300;
}

.heroCard,
.heroCardSecondary {
  position: absolute;
  display: flex;
  flex-direction: column;
  padding: 22px;
  border: 1px solid rgb(255 255 255 / 70%);
  border-radius: 18px;
  backdrop-filter: blur(12px);
  background: rgb(255 255 255 / 78%);
  box-shadow: 0 20px 55px rgb(47 112 183 / 16%);
  color: #174a82;
  gap: 6px;

  span {
    color: #7890a9;
    font-size: 13px;
  }
}

.heroCard {
  top: 272px;
  right: 54px;
  left: 54px;
}

.heroCardSecondary {
  right: 28px;
  bottom: 72px;
}

.section,
.quizSection {
  display: grid;
  gap: 30px;
}

.sectionHeading {
  max-width: 760px;

  h2,
  p {
    margin: 0;
  }

  h2 {
    color: #12315b;
    font-size: clamp(30px, 4vw, 44px);
    letter-spacing: -0.03em;
    line-height: 1.08;
  }

  > p:not(.eyebrow) {
    margin-top: 16px;
  }
}

.featureGrid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;

  article {
    padding: 26px;
    border: 1px solid #e1ebf6;
    border-radius: 18px;
    background: #fff;
  }

  span {
    color: #0877e8;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.12em;
  }

  h3 {
    margin: 18px 0 0;
    color: #17446f;
    font-size: 21px;
  }

  p {
    margin: 12px 0 0;
    color: #738ba6;
    font-size: 14px;
    line-height: 1.6;
  }
}

.note {
  padding: 26px 30px;
  border: 1px solid #cfe3f8;
  border-radius: 18px;
  background: #eaf5ff;
  color: #557493;

  strong {
    color: #0877e8;
  }

  p {
    margin: 8px 0 0;
    line-height: 1.6;
  }
}

.aboutPreview {
  padding: 36px;
  border: 1px solid #e0ebf6;
  border-radius: 20px;
  background: #fff;
  grid-template-columns: repeat(2, minmax(0, 1fr));

  h2,
  p {
    margin: 0;
  }
}

.textLink {
  display: inline-flex;
  margin-top: 18px;
  color: #0877e8;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
}

@media (width <= 900px) {
  .hero {
    min-height: auto;
    grid-template-columns: 1fr;

    > div:first-child {
      padding: 42px 34px;
    }
  }

  .heroVisual {
    display: none;
  }
}

@media (width <= 720px) {
  .page {
    gap: 54px;
  }

  .hero {
    border-radius: 18px;

    > div:first-child {
      padding: 32px 20px;
    }

    h1 {
      font-size: 42px;
    }
  }

  .featureGrid,
  .aboutPreview {
    grid-template-columns: 1fr;
  }

  .aboutPreview {
    padding: 24px;
  }
}
</style>
