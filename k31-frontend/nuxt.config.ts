// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: [
    '@pinia/nuxt',
    '@element-plus/nuxt'
  ],

  elementPlus: {},

  srcDir: 'src',

  routeRules: {
    '/': { ssr: true },
    '/admin/**': { ssr: false }   // админка только клиентская
  }
})
