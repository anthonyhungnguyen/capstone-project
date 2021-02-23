import { createSlice } from "@reduxjs/toolkit"
import { loginApi, signUpApi } from "apis/user"

// Slice

const userData = JSON.parse(localStorage.getItem("user"))

const slice = createSlice({
  name: "login",
  initialState: {
    loginLoading: false,
    loginError: false,
    loginErrorMessage: "",
    signUpLoading: false,
    signUpSuccess: false,
    signUpError: false,
    signUpErrorMessage: "",
    userData: userData ?? null,
    isLoggedIn: userData !== null,
    timestamp: null
  },
  reducers: {
    loginRequested: (state, _) => {
      state.loginLoading = true
    },
    loginSuccess: (state, action) => {
      state.loginLoading = false
      state.isLoggedIn = true
      state.userData = action.payload
      localStorage.setItem("user", JSON.stringify(action.payload))
    },
    loginFail: (state, action) => {
      state.loginLoading = false
      state.loginError = true
      state.loginErrorMessage = action.payload.message
    },
    signUpRequested: (state, _) => {
      state.signUpLoading = true
    },
    signUpSuccess: (state, _) => {
      state.signUpSuccess = true
    },
    signUpFail: (state, action) => {
      state.signUpLoading = false
      state.signUpError = true
      state.signUpErrorMessage = action.payload.message
    },
    logOut: (state, _) => {
      state.isLoggedIn = false
      state.userData = null
      localStorage.setItem("user", null)
    }
  }
})

export default slice.reducer

// Actions

const {
  loginRequested,
  loginSuccess,
  loginFail,
  logOut,
  signUpRequested,
  signUpSuccess,
  signUpFail
} = slice.actions

export const login = data => async dispatch => {
  dispatch(loginRequested())
  await loginApi(data).then(
    result => {
      dispatch(
        loginSuccess({
          accessToken: result.accessToken,
          username: data.username
        })
      )
    },
    error => {
      dispatch(loginFail(error))
    }
  )
}

export const signup = data => async dispatch => {
  dispatch(signUpRequested())
  await signUpApi(data).then(
    () => {
      dispatch(signUpSuccess())
    },
    error => {
      dispatch(signUpFail(error))
    }
  )
}

export const logout = () => dispatch => {
  dispatch(logOut())
}
