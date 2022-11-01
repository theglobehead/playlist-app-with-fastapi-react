import React, { Component } from 'react';
import axios from "axios";
import { Simulate } from "react-dom/test-utils";
import input = Simulate.input;
import Cookies from 'universal-cookie';

const cookies = new Cookies();

type FormState = {
  name: string,
  password: string,
}

export class LoginPage extends Component<{}, FormState> {
  logUserIn() {
    const formData = new FormData();
    formData.append("name", this.state.name)
    formData.append("password", this.state.password)
    formData.append("remember_me", "false")

    axios.post("http://127.0.0.1:8000/login", formData)
    .then(function (response)
    {
      cookies.set("user_uuid", response.data["user_uuid"])
      cookies.set("token_uuid", response.data["token_uuid"])
      window.location.reload();
    })
    .catch(function (error) {
      console.error(error);
    });
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
            <h3>('strings.login')</h3>
            <div className={"form-body"}>
              <div>Username</div>
              <input
                type={"text"}
                style={{marginBottom: "10px"}}
                placeholder={"Username"}
                name={"username"}
                autoComplete={"off"}
                onChange={ e => this.onNameChange(e) }
                required
              />
              <div>Password</div>
              <input
                type={"password"}
                placeholder={"Password"}
                name={"password"}
                autoComplete={"off"}
                onChange={ e => this.onPasswordChange(e) }
                required
              />
            </div>
            <button
                className={"form-bottom-btn btn-scifi"}
                type={"submit"}
                onClick={ () => this.logUserIn() }
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
}
