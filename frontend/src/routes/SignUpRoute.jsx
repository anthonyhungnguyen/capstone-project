import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
const SignUp = lazy(() => import("pages/SignUp"))

export default function SignUpRoute() {
  return (
    <Switch>
      <Route
        path={PATH.COMMON.SIGN_UP}
        component={() => (
          <Suspense fallback={<Loading />}>
            <SignUp />
          </Suspense>
        )}
      />
    </Switch>
  )
}
