import React from "react"
import { BrowserRouter } from "react-router-dom"
import LoginRoute from "./LoginRoute"
import TeacherHomeRoute from "./Teacher/TeacherHomeRoute"
import StudentHomeRoute from "./Student/StudentHomeRoute"
import TeacherScheduleRoute from "./Teacher/TeacherScheduleRoute"

export default function Routes() {
  return (
    <BrowserRouter>
      <LoginRoute />
      <StudentHomeRoute />
      <TeacherHomeRoute />
      <TeacherScheduleRoute />
    </BrowserRouter>
  )
}
