import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import StudentGuard from "guards/StudentGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const ManageUser = lazy(() => import("pages/Admin/ManageUser"))

export default function ManageUserRoute() {
  return (
    <Switch>
      <StudentGuard
        exact
        path={PATH.ADMIN.MANAGE_USER}
        component={() => (
          <Suspense fallback={<Loading />}>
            <ManageUser />
          </Suspense>
        )}
      />
    </Switch>
  )
}
