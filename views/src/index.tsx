import React from 'react';
import ReactDOM from 'react-dom/client';
import "./assets/scss/main.css"

import LoginPage from "./pages/login_page";
import YourPlaylist from "./pages/your_playlist";

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

let loggedIn = false;

root.render(
  <React.StrictMode>
      {!loggedIn &&
          <LoginPage></LoginPage>
      }
      {loggedIn &&
        <YourPlaylist></YourPlaylist>
      }
  </React.StrictMode>
);
