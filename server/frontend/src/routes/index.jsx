import React from "react"
import { BrowserRouter } from "react-router-dom"
import LoginRoute from "./LoginRoute"
import LandingRoute from "./LandingRoute"
import FaceEnrollRoute from "./FaceEnrollRoute"
import FaceProfileRoute from "./FaceProfileRoute"
import ProfileRoute from "./ProfileRoute"
import TeacherHomeRoute from "./Teacher/TeacherHomeRoute"
import TeacherRegisterRoute from "./Teacher/TeacherHomeRegister"
import TeacherManageRoute from "./Teacher/TeacherManageRoute"
import StudentHomeRoute from "./Student/StudentHomeRoute"
import StudentLogsRoute from "./Student/StudentLogsRoute"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <LandingRoute />
      <FaceEnrollRoute />
      <FaceProfileRoute />
      <StudentLogsRoute />
      <ProfileRoute />
      <StudentHomeRoute />
      <TeacherHomeRoute />
      <TeacherRegisterRoute />
      <TeacherManageRoute />
    </BrowserRouter>
  )
}
