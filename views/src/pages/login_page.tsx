import React, {useRef} from 'react';
import axios from "axios";
import {Simulate} from "react-dom/test-utils";
import input = Simulate.input;
import Cookies from 'universal-cookie';
import { useTranslation, Trans } from 'react-i18next';


function LoginPage() {
  const cookies = new Cookies();
  const { t } = useTranslation();

  const logUserIn = async () => {
    const formData = new FormData();
    formData.append("name", usernameRef.current.value)
    formData.append("password", passwordRef.current.value)
    formData.append("remember_me", "false")

    axios.post("http://127.0.0.1:8000/login", formData)
    .then(function (response)
    {
      cookies.set("user_uuid", response.data["user_uuid"])
      cookies.set("token_uuid", response.data["token_uuid"])
      window.location.reload();
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  let usernameRef = useRef(document.createElement("input"))
  let passwordRef = useRef(document.createElement("input"))

  return (
      <div className={"login-main"}>
        <h1 style={{fontSize: "80px"}}>Welcome to the app!</h1>
        <div>
          <div
              className={"rounded-form shadow"}
          >
            <h3>{t('strings.login')}</h3>
            <div className={"form-body"}>
              <div>Username</div>
              <input
                type={"text"}
                style={{marginBottom: "10px"}}
                placeholder={"Username"}
                ref={usernameRef}
                name={"username"}
                autoComplete={"off"}
                required
              />
              <div>Password</div>
              <input
                type={"password"}
                placeholder={"Password"}
                ref={passwordRef}
                name={"password"}
                autoComplete={"off"}
                required
              />
            </div>
            <button
                className={"form-bottom-btn btn-scifi"}
                type={"submit"}
                onClick={() => logUserIn()}
            >
              Log in
            </button>
          </div>
          <p style={{marginTop: "13px", textAlign: "center"}}>
            No account? <a href="#">Register here!</a>
          </p>
        </div>
      </div>
  );
}

export default LoginPage;