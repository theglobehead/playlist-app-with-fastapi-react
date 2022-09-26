import React from 'react';
import ReactDOM from 'react-dom/client';
import "./assets/scss/main.css"
import SidePanel from "./components/side_panel";

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <SidePanel></SidePanel>
  </React.StrictMode>
);
