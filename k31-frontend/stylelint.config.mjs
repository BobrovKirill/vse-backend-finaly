/** @type {import('stylelint').Config} */
export default {
  customSyntax: 'postcss-html',

  extends: [
    'stylelint-config-idiomatic-order',
    'stylelint-config-standard-scss',
    'stylelint-config-recommended-vue/scss',
  ],

  overrides: [
    {
      files: ['*.vue', '**/*.vue'],
      rules: {
        'no-invalid-position-declaration': null,
      },
    },
  ],

  rules: {
    // Чтобы не ругался на @apply
    'at-rule-no-deprecated': null,
    // Можно писать несокращенные свойства
    'declaration-block-no-redundant-longhand-properties': null,
    // Можно делать отступы между css правилами
    'declaration-empty-line-before': null,
    // Чтобы писать css модули в стиле camelСase
    'selector-class-pattern': /.+/,
    // Чтобы не ругался на @tailwind
    'scss/at-rule-no-unknown': null,
  },
}
