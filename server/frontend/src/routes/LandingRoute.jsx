import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"

import Loading from "components/Miscellaneous/Loading"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import PATH from "constants/path"
const Landing = lazy(() => import("pages/Landing"))

export default function LandingRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.COMMON.LANDING}
        component={() => (
          <Suspense fallback={<Loading />}>
            <Landing />
          </Suspense>
        )}
      />
    </Switch>
  )
}
