import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import StudentGuard from "guards/StudentGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const StudentLogs = lazy(() => import("pages/Student/Logs"))

export default function StudentLogsRoute() {
  return (
    <Switch>
      <StudentGuard
        exact
        path={PATH.STUDENT.LOGS}
        component={() => (
          <Suspense fallback={<Loading />}>
            <StudentLogs />
          </Suspense>
        )}
      />
    </Switch>
  )
}
