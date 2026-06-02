<template>
  <div :class="$style.page">
    <section :class="$style.hero">
      <p :class="$style.eyebrow">
        Команда
      </p>
      <h1>Люди, которые развивают K+31</h1>
      <p>
        Пока это каркас страницы. Позже здесь появятся реальные фотографии, роли и короткие рассказы об участниках проекта.
      </p>
    </section>

    <section :class="$style.teamGrid">
      <article>
        <div :class="$style.avatar">АК</div>
        <p :class="$style.role">Продукт</p>
        <h2>Алексей Крылов</h2>
        <p>Исследует пользовательский сценарий и помогает превратить идею в понятный цифровой сервис.</p>
      </article>
      <article>
        <div :class="$style.avatar">МС</div>
        <p :class="$style.role">Разработка</p>
        <h2>Мария Соколова</h2>
        <p>Проектирует интерфейсы и собирает клиентскую часть продукта на Nuxt и Element Plus.</p>
      </article>
      <article>
        <div :class="$style.avatar">ДВ</div>
        <p :class="$style.role">Аналитика</p>
        <h2>Дмитрий Волков</h2>
        <p>Работает со структурой данных и логикой рекомендаций для будущей интеграции с API.</p>
      </article>
      <article :class="$style.joinCard">
        <div :class="$style.joinIcon">+</div>
        <h2>Здесь может быть участник команды</h2>
        <p>Карточки временные: состав, тексты и фотографии можно будет заменить без изменения структуры страницы.</p>
      </article>
    </section>

    <section :class="$style.note">
      <div>
        <p :class="$style.eyebrow">
          Общая цель
        </p>
        <h2>Делаем сложный выбор немного проще</h2>
      </div>
      <p>
        Команда работает над MVP последовательно: сначала проверяем сценарий опроса и рекомендации пакетов, затем подключаем API, административную часть и новые продуктовые разделы.
      </p>
    </section>
  </div>
</template>

<style lang="scss" module>
.page {
  display: grid;
  max-width: 1192px;
  margin: 0 auto;
  gap: 46px;
}

.hero {
  max-width: 850px;
  padding: 36px 0 10px;

  h1 {
    margin: 0;
    color: #12315b;
    font-size: clamp(42px, 6vw, 68px);
    letter-spacing: -0.04em;
    line-height: 1.04;
  }

  > p:not(.eyebrow) {
    margin: 20px 0 0;
    color: #66809f;
    font-size: 17px;
    line-height: 1.65;
  }
}

.eyebrow,
.role {
  margin: 0 0 14px;
  color: #0877e8;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.teamGrid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;

  article {
    padding: 28px;
    border: 1px solid #e1ebf6;
    border-radius: 20px;
    background: #fff;
  }

  h2 {
    margin: 12px 0 0;
    color: #17446f;
    font-size: 24px;
  }

  article > p:not(.role) {
    margin: 12px 0 0;
    color: #738ba6;
    font-size: 14px;
    line-height: 1.65;
  }
}

.avatar,
.joinIcon {
  display: grid;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #eaf5ff;
  color: #0877e8;
  font-size: 22px;
  font-weight: 700;
  place-items: center;
}

.role {
  margin-top: 22px;
  margin-bottom: 0;
  font-size: 11px;
}

.joinCard {
  background: linear-gradient(145deg, #fff, #edf6ff) !important;
}

.joinIcon {
  font-size: 42px;
  font-weight: 300;
}

.note {
  display: grid;
  align-items: center;
  padding: 34px;
  border: 1px solid #cfe3f8;
  border-radius: 20px;
  background: #eaf5ff;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 32px;

  h2,
  p {
    margin: 0;
  }

  h2 {
    color: #17446f;
    font-size: 30px;
  }

  > p {
    color: #557493;
    line-height: 1.65;
  }
}

@media (width <= 700px) {
  .hero {
    padding-top: 18px;
  }

  .teamGrid,
  .note {
    grid-template-columns: 1fr;
  }

  .note {
    padding: 24px;
    gap: 14px;
  }
}
</style>
