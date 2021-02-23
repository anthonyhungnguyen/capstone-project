import React from "react"
import { BrowserRouter } from "react-router-dom"
import SignUpRoute from "./SignUpRoute"
import LoginRoute from "./LoginRoute"
import HomeRoute from "./HomeRoute"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <SignUpRoute />
      <HomeRoute />
    </BrowserRouter>
  )
}
