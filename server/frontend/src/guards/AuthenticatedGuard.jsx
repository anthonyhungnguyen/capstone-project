import PATH from "constants/path"
import React from "react"
import { useSelector } from "react-redux"
import { Redirect, Route } from "react-router-dom"

export default function AuthenticatedGuard(children) {
  const { component: Component, ...rest } = children
  const { isLoggedIn } = useSelector(state => state.auth)
  return (
    <Route
      {...rest}
      render={props => {
        if (!isLoggedIn && !localStorage.getItem("user")) {
          return <Redirect to={PATH.COMMON.LOGIN} />
        }
        return <Component {...props} />
      }}
    />
  )
}
