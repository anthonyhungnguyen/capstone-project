import FooterBar from "components/Miscellaneous/FooterBar"
import HeaderBar from "components/Miscellaneous/HeaderBar"
import React from "react"

export default function MainLayout(props) {
  const { children } = props
  return (
    <div>
      <HeaderBar />
      <div className="container mx-auto p-10">{children}</div>
      {/* <FooterBar /> */}
    </div>
  )
}
