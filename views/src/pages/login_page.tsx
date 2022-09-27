import React from 'react';

function LoginPage() {
  return (
      <div className={"login-main"}>
        <h1 style={{fontSize: "80px"}}>Welcome to the app!</h1>
        <div>
          <form
              className={"rounded-form shadow"}
              action={""}
              method={"post"}
          >
            <h3>Login</h3>
            <div className={"form-body"}>
              <div>Username</div>
              <input
                type={"text"}
                style={{marginBottom: "10px"}}
                placeholder={"Username"}
                id={"username_input"}
                name={"username"}
                autoComplete={"off"}
                required
              />
              <div>Password</div>
              <input
                type={"password"}
                placeholder={"Password"}
                id={"password_input"}
                name={"password"}
                autoComplete={"off"}
                required
              />
            </div>
            <button
                className={"form-bottom-btn btn-scifi"}
                type={"submit"}
            >
              Log in
            </button>
          </form>
          <p style={{marginTop: "13px", textAlign: "center"}}>
            No account? <a href="#">Register here!</a>
          </p>
        </div>
      </div>
  );
}

export default LoginPage;