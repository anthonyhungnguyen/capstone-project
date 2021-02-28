import Loading from "components/Miscellaneous/Loading"
import { PATH } from "constants/path"
import AuthenticatedGuard from "guards/AuthenticatedGuard"
import FaceProfile from "pages/FaceProfile"
import React, { Suspense } from "react"
import { Switch } from "react-router-dom"

export default function FaceProfileRoute() {
  return (
    <Switch>
      <AuthenticatedGuard
        exact
        path={PATH.FACE_PROFILE}
        component={() => (
          <Suspense fallback={<Loading />}>
            <FaceProfile />
          </Suspense>
        )}
      />
    </Switch>
  )
}
