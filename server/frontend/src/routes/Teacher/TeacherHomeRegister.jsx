import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import TeacherGuard from "guards/TeacherGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const TeacherRegister = lazy(() => import("pages/Teacher/Register"))

export default function TeacherRegisterRoute() {
  return (
    <Switch>
      <TeacherGuard
        exact
        path={PATH.TEACHER.REGISTER}
        component={() => (
          <Suspense fallback={<Loading />}>
            <TeacherRegister />
          </Suspense>
        )}
      />
    </Switch>
  )
}
