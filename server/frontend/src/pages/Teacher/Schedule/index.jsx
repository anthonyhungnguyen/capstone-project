import TeacherManage from "components/Schedule/Manage"
import TeacherRegister from "components/Schedule/Register"
import MainLayout from "layouts/MainLayout"
import React from "react"

export default function Schedule() {
  return (
    <MainLayout>
      <TeacherRegister />
      <TeacherManage />
    </MainLayout>
  )
}
