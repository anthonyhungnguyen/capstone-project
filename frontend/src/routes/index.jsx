import React from "react"
import { BrowserRouter } from "react-router-dom"
import SignUpRoute from "./SignUpRoute"
import LoginRoute from "./LoginRoute"
import LandingRoute from "./LandingRoute"
import FaceEnrollRoute from "./FaceEnrollRoute"
import FaceProfileRoute from "./FaceProfileRoute"
import ProfileRoute from "./ProfileRoute"
import TeacherHomeRoute from "./Teacher/TeacherHomeRoute"
import TeacherRegisterRoute from "./Teacher/TeacherHomeRegister"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <SignUpRoute />
      <LandingRoute />
      <FaceEnrollRoute />
      <FaceProfileRoute />
      <ProfileRoute />
      <TeacherHomeRoute />
      <TeacherRegisterRoute />
    </BrowserRouter>
  )
}
