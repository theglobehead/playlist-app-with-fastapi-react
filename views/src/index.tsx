import React from 'react';
import ReactDOM from 'react-dom/client';
import "./assets/scss/main.css"
import Cookies from 'universal-cookie';
import './i18n';

import { LoginPage } from "./pages/login_page";
import { YourPlaylists } from "./pages/your_playlist";

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const cookies = new Cookies();
let loggedIn = cookies.get("user_uuid");

root.render(
  <React.StrictMode>
      {!loggedIn &&
          <LoginPage></LoginPage>
      }
      {loggedIn &&
         <YourPlaylists></YourPlaylists>
      }
  </React.StrictMode>
);
