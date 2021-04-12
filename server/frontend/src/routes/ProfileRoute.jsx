import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router"
const Profile = lazy(() => import("pages/Profile"))

export default function ProfileRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.COMMON.PROFILE}
        component={() => (
          <Suspense fallback={<Loading />}>
            <Profile />
          </Suspense>
        )}
      />
    </Switch>
  )
}
