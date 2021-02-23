import { PATH } from "constants/path"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { useForm } from "react-hook-form"
import { useDispatch, useSelector } from "react-redux"
import { useHistory } from "react-router-dom"
import { signup } from "store/user"

function SignUp() {
  const { register, handleSubmit, watch, errors } = useForm()
  const dispatch = useDispatch()
  const history = useHistory()
  const {
    signUpLoading,
    signUpSuccess,
    signUpError,
    signUpErrorMessage
  } = useSelector(state => state.user)

  const onSubmit = data => {
    dispatch(signup(data))
  }

  if (signUpSuccess) {
    history.push(PATH.LOGIN)
  }

  return (
    <MainLayout>
      {signUpLoading && <p>Loading</p>}
      {signUpError && <p>{signUpErrorMessage}</p>}
      <form onSubmit={handleSubmit(onSubmit)}>
        <label>ID</label>
        <input
          name="id"
          type="text"
          ref={register({ required: "You must specify ID" })}
        />
        {errors.id?.message}
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
        {errors.password?.message}
        <label>Repeat password</label>
        <input
          name="repeatPassword"
          type="password"
          ref={register({
            validate: value =>
              value === watch("password") || "Repeat password does not match"
          })}
        />
        {errors.repeatPassword?.message}

        <input type="submit" />
      </form>
    </MainLayout>
  )
}

export default SignUp
