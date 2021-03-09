import PATH from "constants/path"
import React, { useState } from "react"
import { useForm } from "react-hook-form"
import { useDispatch, useSelector } from "react-redux"
import { useHistory } from "react-router-dom"
import { signup } from "slices/auth"

function SignUp() {
  const [loading, setLoading] = useState(false)
  const [fail, setFail] = useState(false)
  const { register, handleSubmit, watch, errors } = useForm()
  const dispatch = useDispatch()
  const history = useHistory()
  const { isLoggedIn } = useSelector(state => state.auth)
  const { message } = useSelector(state => state.message)

  const onSubmit = data => {
    setLoading(true)
    dispatch(signup(data))
      .then(() => {
        setLoading(false)
        history.push(PATH.LOGIN)
      })
      .catch(() => {
        setLoading(false)
        setFail(true)
      })
  }

  if (isLoggedIn) {
    history.push(PATH.HOME)
  }

  const onSignIn = () => {
    history.push(PATH.COMMON.LOGIN)
  }

  return (
    <>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          {fail ? (
            <p className="text-center text-md text-white bg-red-500 border border-gray-200 rounded-md p-2">
              {message}
            </p>
          ) : null}
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{" "}
            <button
              onClick={onSignIn}
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              sign in here
            </button>
          </p>
          <div className="bg-white p-8 shadow-lg rounded-md border">
            <form className="space-y-8" onSubmit={handleSubmit(onSubmit)}>
              <div>
                <label htmlFor="id" className="sr-only">
                  ID
                </label>

                <input
                  id="id"
                  name="id"
                  type="text"
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="ID"
                  ref={register({
                    required: "You must specify username",
                    pattern: {
                      value: /^[0-9]+$/i,
                      message: "Username must be number"
                    }
                  })}
                />
                <p className="text-sm font-medium text-red-400  ml-2 mt-2">
                  {errors.id?.message}
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
                    required: "You must specify password",
                    minLength: {
                      value: 8,
                      message: "Your password must be at least 8 characters"
                    }
                  })}
                />
                <p className="text-sm font-medium text-red-400  ml-2 mt-2">
                  {errors.password?.message}
                </p>
              </div>
              <div>
                <label htmlFor="repeatPassword" className="sr-only">
                  Repeat password
                </label>

                <input
                  id="repeatPassword"
                  name="repeatPassword"
                  type="password"
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Repeat password"
                  ref={register({
                    validate: value =>
                      value === watch("password") ||
                      "Repeat password does not match"
                  })}
                />
                <p className="text-sm font-medium text-red-400 ml-2 mt-2">
                  {errors.repeatPassword?.message}
                </p>
              </div>
              <div>
                <button
                  type="submit"
                  className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-sm text-white bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                    {/* <!-- Heroicon name: solid/lock-closed --> */}
                    {loading ? (
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
                  Sign up
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}

export default SignUp
