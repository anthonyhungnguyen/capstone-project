import FooterBar from "components/FooterBar"
import HeaderBar from "components/HeaderBar"
import React from "react"

export default function MainLayout(props) {
  const { children } = props
  return (
    <div>
      <HeaderBar />
      {children}
      {/* <FooterBar /> */}
    </div>
  )
}
