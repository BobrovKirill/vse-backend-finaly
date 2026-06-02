# Архитектура базы данных

## ERD-диаграмма

```mermaid
erDiagram
    USERS {
        int id PK
        string email UK
        string hashed_password
        bool is_admin
        datetime created_at
    }

    QUESTIONS {
        int id PK
        text text
        text help_text
        string question_type
        int position
        bool is_active
        datetime created_at
    }

    ANSWERS {
        int id PK
        int question_id FK
        text text
        text description
        int position
        bool is_active
    }

    HEALTH_INDICATORS {
        int id PK
        string code UK
        string title
        text description
        bool is_active
        datetime created_at
    }

    ANSWER_EFFECTS {
        int id PK
        int answer_id FK
        int indicator_id FK
        int score
    }

    PACKAGES {
        int id PK
        string title
        text description
        numeric price
        string checkout_url
        bool is_active
        datetime created_at
    }

    SERVICES {
        int id PK
        string title
        text description
        numeric price
        bool is_active
        datetime created_at
    }

    PACKAGES_SERVICES {
        int id PK
        int package_id FK
        int service_id FK
        int position
    }

    PACKAGE_RULES {
        int id PK
        int package_id FK
        int indicator_id FK
        int min_score
        int max_score
        int weight
    }

    CHOICES {
        int id PK
        string contact_name
        string contact_phone
        datetime created_at
    }

    CHOICES_ANSWERS {
        int id PK
        int choice_id FK
        int answer_id FK
    }

    CHOICES_INDICATOR_SCORES {
        int id PK
        int choice_id FK
        int indicator_id FK
        int score
    }

    CHOICES_PACKAGE_RECOMMENDATIONS {
        int id PK
        int choice_id FK
        int package_id FK
        int rank
        int matched_weight
    }

    QUESTIONS ||--o{ ANSWERS : has
    ANSWERS ||--o{ ANSWER_EFFECTS : produces
    HEALTH_INDICATORS ||--o{ ANSWER_EFFECTS : receives
    PACKAGES ||--o{ PACKAGE_RULES : has
    HEALTH_INDICATORS ||--o{ PACKAGE_RULES : checks
    PACKAGES ||--o{ PACKAGES_SERVICES : contains
    SERVICES ||--o{ PACKAGES_SERVICES : included_in
    CHOICES ||--o{ CHOICES_ANSWERS : contains
    ANSWERS ||--o{ CHOICES_ANSWERS : selected
    CHOICES ||--o{ CHOICES_INDICATOR_SCORES : stores
    HEALTH_INDICATORS ||--o{ CHOICES_INDICATOR_SCORES : scored
    CHOICES ||--o{ CHOICES_PACKAGE_RECOMMENDATIONS : receives
    PACKAGES ||--o{ CHOICES_PACKAGE_RECOMMENDATIONS : recommended_as
```

## Описание связей

### Questions -> Answers

Один вопрос содержит несколько вариантов ответа.

```text
Имеете ли вы лишний вес?
  Нет
  Немного
  Есть
  Сильный
```

### Answers -> AnswerEffects

Один ответ может содержать несколько эффектов. Эффект показывает, какой индикатор изменяется и сколько баллов добавляется.

```text
Ответ: "Плохой сон"
  Сон +2
  Стресс +1
```

### HealthIndicators -> AnswerEffects

Один медицинский индикатор может получать баллы от разных ответов и разных вопросов.

```text
Индикатор: Риск диабета
  +1 от ответа про наследственность
  +2 от ответа про лишний вес
```

### Packages -> PackageRules

Один пакет содержит несколько правил подбора.

```text
Пакет: Диабет-скрининг
  Риск диабета >= 2
  Лишний вес >= 2
```

### HealthIndicators -> PackageRules

Каждое правило проверяет значение конкретного индикатора. Вопросы и ответы напрямую с пакетами не связаны.

### Choices -> ChoicesAnswers

`Choice` - одно полное прохождение опроса пользователем. Оно содержит выбранные ответы.

```text
Прохождение #1:
  Вопрос про вес -> "Есть"
  Вопрос про сон -> "Плохой сон"
```

### Answers -> ChoicesAnswers

Таблица `choices_answers` хранит ссылки на ответы, выбранные в конкретном прохождении.

### Choices -> ChoicesIndicatorScores

После завершения опроса система суммирует эффекты ответов и сохраняет итоговые баллы индикаторов.

```text
Прохождение #1:
  Лишний вес = 2
  Сон = 2
  Стресс = 1
```

### HealthIndicators -> ChoicesIndicatorScores

Каждая итоговая оценка относится к одному индикатору.

### Packages -> PackagesServices -> Services

Услуги хранятся структурированно. Один пакет может содержать несколько услуг, а одна услуга может входить в разные пакеты. Общая цена пакета хранится отдельно от необязательных цен отдельных услуг.

### Choices -> ChoicesPackageRecommendations

После анализа система сохраняет несколько подходящих пакетов в порядке релевантности. У каждой рекомендации есть позиция `rank` и сумма весов совпавших правил `matched_weight`.

### Users

Отдельная таблица администраторов. Админы входят в систему и управляют вопросами, ответами, эффектами, индикаторами и пакетами. С прохождениями пользователей она напрямую не связана.

## Поток анализа

```text
Вопросы
  -> выбранные ответы
  -> эффекты ответов
  -> итоговые баллы индикаторов
  -> проверка правил пакетов
  -> ранжированный список рекомендованных пакетов
```

## Нормализация

Модель соответствует третьей нормальной форме (3NF):

- связи many-to-many вынесены в отдельные таблицы;
- вопросы и ответы напрямую не связаны с пакетами;
- услуги пакетов вынесены в отдельный справочник;
- в `choices_answers` не хранится `question_id`, потому что вопрос определяется через `answer_id`;
- общий балл прохождения не хранится отдельно, а вычисляется из `choices_indicator_scores`.

`choices_indicator_scores` хранит снимок результата анализа на момент прохождения опроса. Это позволяет сохранить историю, даже если администратор позднее изменит эффекты ответов.

## Redis-кеш

Публичная анкета кешируется в Redis:

```text
GET /api/v1/public/questions
  -> Redis: public:questions:v1
  -> при отсутствии ключа читаем PostgreSQL
  -> сохраняем публичный JSON в Redis на 600 секунд
```

После создания, изменения или удаления вопроса или ответа ключ удаляется. При недоступности Redis публичный API продолжает работать через PostgreSQL.
