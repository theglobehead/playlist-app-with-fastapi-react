import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    debug: false,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
    resources: {
      en: {
        translation: {
          "strings.login": "Login",
          "strings.username": "Username",
          "strings.password": "Password",
          "strings.no_account": "No account?",
          "strings.log_in": "Log in",
          "strings.log_out": "Log out",
          "strings.register_here": "Register here!",
          "strings.playlists": "Playlists",
          "strings.settings": "Settings",
          "strings.discover": "Discover",
          "strings.artists" : "Artists",
        }
      }
    }
  });

export default i18n;
