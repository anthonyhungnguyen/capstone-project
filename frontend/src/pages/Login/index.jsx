import { Button, Card } from "antd"
import { PATH } from "constants/path"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { useForm } from "react-hook-form"
import { useDispatch, useSelector } from "react-redux"
import { useHistory } from "react-router-dom"
import { login } from "slices/user"

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

  const onSignUp = () => {
    history.push(PATH.SIGN_UP)
  }

  if (isLoggedIn) {
    history.push(PATH.HOME)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {loginError === true ? (
          <p className="text-center text-md text-white bg-red-500 border border-gray-200 rounded-md p-2">
            {loginErrorMessage}
          </p>
        ) : null}
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{" "}
          <button
            onClick={onSignUp}
            className="font-medium text-indigo-600 hover:text-indigo-500"
          >
            sign up here
          </button>
        </p>
        <div className="bg-white p-8 shadow-lg rounded-md border">
          <form className="space-y-8" onSubmit={handleSubmit(onSubmit)}>
            <div>
              <label htmlFor="username" className="sr-only">
                ID
              </label>

              <input
                id="username"
                name="username"
                type="text"
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Username"
                ref={register({
                  required: "You must specify username",
                  pattern: {
                    value: /^[0-9]+$/i,
                    message: "Username must be number"
                  }
                })}
              />
              <p className="text-sm font-medium text-red-400  ml-2 mt-2">
                {errors.username?.message}
              </p>
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>

              <input
                id="password"
                name="password"
                type="password"
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                ref={register({
                  required: "You must specify password"
                })}
              />
              <p className="text-sm font-medium text-red-400  ml-2 mt-2">
                {errors.password?.message}
              </p>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember_me"
                  name="remember_me"
                  type="checkbox"
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label
                  id="remember_me"
                  className="ml-2 block text-sm text-gray-900"
                >
                  Remember me
                </label>
              </div>
              <div className="text-sm">
                <button className="font-medium text-indigo-600 hover:text-indigo-500">
                  Forgot your password?
                </button>
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-sm text-white bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                  {/* <!-- Heroicon name: solid/lock-closed --> */}
                  {loginLoading ? (
                    <svg
                      class="animate-spin h-5 w-5 mr-3"
                      viewBox="0 0 24 24"
                    ></svg>
                  ) : (
                    <svg
                      className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        fillRule="evenodd"
                        d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </span>
                Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login