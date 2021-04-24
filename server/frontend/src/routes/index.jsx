import React from "react"
import { BrowserRouter, Redirect } from "react-router-dom"
import LoginRoute from "./LoginRoute"
import TeacherHomeRoute from "./Teacher/TeacherHomeRoute"
import StudentHomeRoute from "./Student/StudentHomeRoute"
import TeacherScheduleRoute from "./Teacher/TeacherScheduleRoute"
import PATH from "constants/path"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <StudentHomeRoute />
      <TeacherHomeRoute />
      <TeacherScheduleRoute />
      <Redirect to={PATH.COMMON.LOGIN} />
    </BrowserRouter>
  )
}
