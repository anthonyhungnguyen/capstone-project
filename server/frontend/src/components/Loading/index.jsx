import React from "react"
import { css } from "@emotion/core"
import ClimbingBoxLoader from "react-spinners/ClimbingBoxLoader"

export default function Loading() {
  const override = css`
    display: block;
    margin: auto;
    border-color: red;
  `
  return (
    <div className="h-screen flex items-center">
      <ClimbingBoxLoader loading={true} size={30} css={override} />
    </div>
  )
}
