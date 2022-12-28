import React, { Component } from 'react';
import axios from "axios";
import { Simulate } from "react-dom/test-utils";
import input = Simulate.input;
import Cookies from 'universal-cookie';
import i18n from 'i18next';

const cookies = new Cookies();

type Props = {
  name: string,
  password: string,
  isMessageVisible: boolean,
}

type State = {
  name: string,
  password: string,
  isMessageVisible: boolean,
}

export class LoginPage extends Component<{}, State> {

  constructor(props: Props) {
    super(props);
    this.state = {
      name: "",
      password: "",
      isMessageVisible: false
    }
  }

  async logInUser(){
    try{
      const formData = new FormData();
      formData.append("name", this.state.name.trim())
      formData.append("password", this.state.password.trim())
      formData.append("remember_me", "false")

      let response = await axios.post("http://127.0.0.1:8000/login", formData)

      if (response.data.message === "success"){
        cookies.set("user_uuid", response.data["user_uuid"])
        cookies.set("token_uuid", response.data["token_uuid"])
        window.location.reload();
      }else{
        this.setState({"isMessageVisible": true })
      }
    }catch (e){
      console.error(e)
    }
  }

  onNameChange(event: any){
    this.setState({"name": event.target.value })
  }

  onPasswordChange(event: any){
    this.setState({"password": event.target.value })
  }

  render() {

    return (
      <div className={"login-main"}>
        <h1 style={{fontSize: "80px"}}>Welcome to the app!</h1>
        <div>
          <div
              className={"rounded-form shadow"}
          >
            <h3>{ i18n.t("strings.login") as string }</h3>
            <div className={"form-body"}>
              <div>{ i18n.t('strings.username') as string }</div>
              <input
                type={"text"}
                style={{marginBottom: "10px"}}
                placeholder={"Username"}
                name={"username"}
                autoComplete={"off"}
                onChange={ e => this.onNameChange(e) }
                required
              />
              <div>{ i18n.t("strings.password") as string }</div>
              <input
                type={"password"}
                placeholder={"Password"}
                name={"password"}
                autoComplete={"off"}
                onChange={ e => this.onPasswordChange(e) }
                required
              />
            </div>
            <div
                id={"loginMessage"}
                className={`form-message ${this.state.isMessageVisible ? "" : "hidden"}`}
            >
              { i18n.t("strings.incorrect_login_details") as string }
            </div>
            <button
                className={"form-bottom-btn btn-scifi"}
                type={"submit"}
                onClick={ () => this.logInUser() }
            >
              { i18n.t("strings.log_in") as string }
            </button>
          </div>
          <p style={{marginTop: "13px", textAlign: "center"}}>
            { i18n.t("strings.no_account") as string }
            <a href="#">{ i18n.t("strings.register_here") as string }</a>
          </p>
        </div>
      </div>
    );
  }
}
