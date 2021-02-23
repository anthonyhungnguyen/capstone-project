import { Menu, Layout, Row, Col, Button } from "antd"
import { PATH } from "constants/path"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { useLocation, useHistory } from "react-router-dom"
import { logout } from "store/user"

const { Header } = Layout

export default function HeaderBar() {
  const dispatch = useDispatch()
  const history = useHistory()
  const location = useLocation()
  const { isLoggedIn, userData } = useSelector(state => state.user)
  const { pathname } = location

  // Check whether username exists in store
  // If yes, render Home navbar
  // If no, render Login/SignUp navbar

  const onLogout = () => dispatch(logout())
  const onToSignUpPage = () => history.push(PATH.SIGN_UP)
  const onToLoginPage = () => history.push(PATH.LOGIN)

  return (
    <Header>
      <div className="logo" />
      {isLoggedIn ? (
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
          <Menu.Item key="1">Home</Menu.Item>
          <Menu.Item key="2" style={{ float: "right" }} onClick={onLogout}>
            Logout
          </Menu.Item>
          <Menu.Item style={{ float: "right" }}>
            Hi, {userData?.username}
          </Menu.Item>
        </Menu>
      ) : (
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
          {pathname === PATH.SIGN_UP && (
            <Menu.Item
              key="1"
              style={{ float: "right" }}
              onClick={onToLoginPage}
            >
              Login
            </Menu.Item>
          )}
          {pathname === PATH.LOGIN && (
            <Menu.Item
              key="1"
              style={{ float: "right" }}
              onClick={onToSignUpPage}
            >
              Sign Up
            </Menu.Item>
          )}
        </Menu>
      )}
    </Header>
  )
}
