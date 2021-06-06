import Loading from "components/Loading"
import PATH from "constants/path"
import StudentGuard from "guards/StudentGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const StudentHome = lazy(() => import("pages/Student.jsx"))

export default function StudentHomeRoute() {
  return (
    <Switch>
      <StudentGuard
        exact
        path={PATH.STUDENT.HOME}
        component={() => (
          <Suspense fallback={<Loading />}>
            <StudentHome />
          </Suspense>
        )}
      />
    </Switch>
  )
}
