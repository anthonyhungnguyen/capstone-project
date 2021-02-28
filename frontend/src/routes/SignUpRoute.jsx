import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import { PATH } from "constants/path"
import Loading from "components/Miscellaneous/Loading"
const SignUp = lazy(() => import("pages/SignUp"))

export default function SignUpRoute() {
  return (
    <Switch>
      <Route
        path={PATH.SIGN_UP}
        component={() => (
          <Suspense fallback={<Loading />}>
            <SignUp />
          </Suspense>
        )}
      />
    </Switch>
  )
}
