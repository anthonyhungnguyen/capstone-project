import PATH from "constants/path"
import React, { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Redirect, Route } from "react-router-dom"
import { verify } from "slices/auth"

export default function AuthenticatedGuard(children) {
  const dispatch = useDispatch()
  const { component: Component, ...rest } = children
  const { isLoggedIn } = useSelector(state => state.auth)

  useEffect(() => {
    dispatch(verify())
  }, [])

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
