import Loading from "components/Miscellaneous/Loading"
import PATH from "constants/path"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import React, { lazy, Suspense } from "react"
import { Switch } from "react-router-dom"
const FaceProfile = lazy(() => import("pages/Student/FaceProfile"))

export default function FaceProfileRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.STUDENT.FACE_PROFILE}
        component={() => (
          <Suspense fallback={<Loading />}>
            <FaceProfile />
          </Suspense>
        )}
      />
    </Switch>
  )
}
