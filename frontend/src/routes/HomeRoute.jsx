import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import { PATH } from "constants/path"
import Loading from "components/Miscellaneous/Loading"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
const Home = lazy(() => import("pages/Home"))

export default function HomeRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.HOME}
        component={() => (
          <Suspense fallback={<Loading />}>
            <Home />
          </Suspense>
        )}
      />
    </Switch>
  )
}
