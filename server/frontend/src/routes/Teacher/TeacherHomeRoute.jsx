import Loading from "components/Loading"
import PATH from "constants/path"
import TeacherGuard from "guards/TeacherGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const TeacherHome = lazy(() => import("pages/Teacher/Home"))

export default function TeacherHomeRoute() {
  return (
    <Switch>
      <TeacherGuard
        exact
        path={PATH.TEACHER.HOME}
        component={() => (
          <Suspense fallback={<Loading />}>
            <TeacherHome />
          </Suspense>
        )}
      />
    </Switch>
  )
}
