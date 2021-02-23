import { Button, Card } from "antd"
import { PATH } from "constants/path"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { useForm } from "react-hook-form"
import { useDispatch, useSelector } from "react-redux"
import { useHistory } from "react-router-dom"
import { login } from "store/user"

function Login() {
  const { register, handleSubmit, errors } = useForm()
  const dispatch = useDispatch()
  const history = useHistory()
  const {
    isLoggedIn,
    loginLoading,
    loginError,
    loginErrorMessage
  } = useSelector(state => state.user)

  const onSubmit = data => {
    dispatch(login(data))
  }

  if (isLoggedIn) {
    history.push(PATH.HOME)
  }
  return (
    <MainLayout>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "85vh"
        }}
      >
        <Card title="Login form" style={{ width: 300 }}>
          <form
            onSubmit={handleSubmit(onSubmit)}
            style={{ display: "flex", flexDirection: "column" }}
          >
            {/* Register input into hook */}
            <label>Username</label>
            <input
              name="username"
              type="text"
              ref={register({ required: "You must specify username" })}
            />
            {errors.username?.message}
            <label>Password</label>
            <input
              name="password"
              type="password"
              ref={register({ required: "You must specify password" })}
            />
            {/* Errors will return when field validation fails */}
            {errors.password?.message}
            <button type="submit">Submit</button>
          </form>
        </Card>
      </div>
    </MainLayout>
  )
}

export default Login
