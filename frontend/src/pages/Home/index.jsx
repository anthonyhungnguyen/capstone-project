import { PATH } from "constants/path"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { useSelector } from "react-redux"
import { useHistory } from "react-router-dom"

export default function Home() {
  const { isLoggedIn } = useSelector(state => state.user)
  const history = useHistory()
  if (!isLoggedIn) {
    history.push(PATH.LOGIN)
  }
  return (
    <MainLayout>
      <div>This is home</div>
    </MainLayout>
  )
}
