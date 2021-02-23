import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import { PATH } from "constants/path"
import Loading from "components/Loading"
const Login = lazy(() => import("pages/Login"))

export default function LoginRoute() {
  return (
    <Switch>
      <Route
        path={PATH.LOGIN}
        component={() => (
          <Suspense fallback={<Loading />}>
            <Login />
          </Suspense>
        )}
      />
    </Switch>
  )
}
