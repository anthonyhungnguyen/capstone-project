import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import Loading from "components/Miscellaneous/Loading"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import PATH from "constants/path"
const FaceEnroll = lazy(() => import("pages/Student/FaceEnroll"))

export default function FaceEnrollRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.STUDENT.FACE_ENROLL}
        component={() => (
          <Suspense fallback={<Loading />}>
            <FaceEnroll />
          </Suspense>
        )}
      />
    </Switch>
  )
}
