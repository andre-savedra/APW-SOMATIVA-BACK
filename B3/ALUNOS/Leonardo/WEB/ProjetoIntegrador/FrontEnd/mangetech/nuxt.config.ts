// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  app: {
    head: {
      title: 'Mangetech',
      htmlAttrs: {
        lang: "pt-br"
      },
    }
  },
  components: true,
  modules: [
    '@primevue/nuxt-module',
    '@nuxtjs/google-fonts',
    //'@sidebase/nuxt-auth'
  ],
  css: [
    "@/assets/reset.scss",
    "@/assets/variables.scss",
    "@/assets/global.scss",
  ],
  primevue:{
    components: {
      include: ['Knob']
    },
    options: {
      theme: {
        preset: Aura,
      }
    }
  },
  googleFonts: {
    families: {
      Roboto: true,
      "Varela+Round": true,
    },
  }
})
