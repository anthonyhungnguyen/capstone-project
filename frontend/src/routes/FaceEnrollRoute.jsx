import React, { lazy, Suspense } from "react"
import { Switch, Route } from "react-router-dom"
import { PATH } from "constants/path"
import Loading from "components/Miscellaneous/Loading"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import FaceEnroll from "pages/FaceEnroll"

export default function FaceEnrollRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.FACE_ENROLL}
        component={() => (
          <Suspense fallback={<Loading />}>
            <FaceEnroll />
          </Suspense>
        )}
      />
    </Switch>
  )
}
