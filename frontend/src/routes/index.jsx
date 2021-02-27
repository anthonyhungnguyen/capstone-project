import React from "react"
import { BrowserRouter } from "react-router-dom"
import SignUpRoute from "./SignUpRoute"
import LoginRoute from "./LoginRoute"
import HomeRoute from "./HomeRoute"
import FaceEnrollRoute from "./FaceEnrollRoute"
import FaceProfileRoute from "./FaceProfileRoute"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <SignUpRoute />
      <HomeRoute />
      <FaceEnrollRoute />
      <FaceProfileRoute />
    </BrowserRouter>
  )
}
