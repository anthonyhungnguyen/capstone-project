import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import TeacherGuard from "guards/TeacherGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const TeacherManage = lazy(() => import("pages/Teacher/Manage"))

export default function TeacherManageRoute() {
  return (
    <Switch>
      <TeacherGuard
        exact
        path={PATH.TEACHER.MANAGE}
        component={() => (
          <Suspense fallback={<Loading />}>
            <TeacherManage />
          </Suspense>
        )}
      />
    </Switch>
  )
}
