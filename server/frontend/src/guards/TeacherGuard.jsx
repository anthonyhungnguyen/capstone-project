import PATH from "constants/path"
import ROLE from "constants/role"
import React, { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Redirect, Route } from "react-router"
import { verify } from "slices/auth"

export default function TeacherGuard(children) {
  const { component: Component, ...rest } = children
  const dispatch = useDispatch()
  const { user } = useSelector(state => state.auth)
  useEffect(() => {
    dispatch(verify())
  }, [dispatch])
  return (
    <Route
      {...rest}
      render={props => {
        if (
          !user?.isLoggedIn &&
          !localStorage.getItem("user") &&
          !user?.roles.includes(ROLE.TEACHER)
        ) {
          return <Redirect to={PATH.COMMON.LOGIN} />
        }
        return <Component {...props} />
      }}
    />
  )
}
