import Loading from "components/Loading"
import PATH from "constants/path"
import TeacherGuard from "guards/TeacherGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const TeacherSchedule = lazy(() => import("pages/Teacher/Schedule"))

export default function TeacherScheduleRoute() {
  return (
    <Switch>
      <TeacherGuard
        exact
        path={PATH.TEACHER.SCHEDULE}
        component={() => (
          <Suspense fallback={<Loading />}>
            <TeacherSchedule />
          </Suspense>
        )}
      />
    </Switch>
  )
}
