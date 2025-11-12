// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  app: {
    head: {
      title: "MangeTech", //Nome do Site
      htmlAttrs: {
        lang: "pt-br", //Idioma        
      },
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.png" }],
    }
  },
  modules: [
    '@primevue/nuxt-module', 
    '@nuxtjs/google-fonts'
  ],
  css: [ //aqui puxamos o css na ordem que queremos
    "@/assets/reset.scss",
    "@/assets/variables.scss",
    "@/assets/global.scss",
  ],
    googleFonts: { //fontes do pacote que iremos usar
    families: {
      Roboto: true,
      "Varela Round": true,
    }
  },
  primevue: {
    components: {
      include: ['Knob'],
    },
    options: {
      theme: {
        preset: Aura,
      }
    }
  }
})