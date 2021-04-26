import React from "react"
import { BrowserRouter, Redirect } from "react-router-dom"
import LoginRoute from "./LoginRoute"
import TeacherHomeRoute from "./TeacherHomeRoute"
import StudentHomeRoute from "./StudentHomeRoute"
import PATH from "constants/path"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <StudentHomeRoute />
      <TeacherHomeRoute />
      <Redirect to={PATH.COMMON.LOGIN} />
    </BrowserRouter>
  )
}
