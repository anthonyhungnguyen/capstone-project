import PhotoUpload from "components/Face/PhotoUpload"
import WebcamCapture from "components/Webcam"
import React from "react"
import { useSelector } from "react-redux"

export default function Upload() {
  const { input } = useSelector(state => state.faceEnroll)

  return input === "Webcam" ? <WebcamCapture /> : <PhotoUpload />
}
