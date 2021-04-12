import { Button } from "antd"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { inputUpdate } from "slices/faceEnroll.js"

export default function ChooseInput() {
  const dispatch = useDispatch()
  const { input } = useSelector(state => state.faceEnroll)

  const onChangeEnrollMethod = enrollMethod => {
    dispatch(inputUpdate(enrollMethod))
  }

  return (
    <div className="flex items-center justify-between flex-col space-y-8 m-auto">
      <Button
        className="w-1/3"
        type={`${input === "Webcam" ? "primary" : "ghost"}`}
        onClick={() => onChangeEnrollMethod("Webcam")}
      >
        Webcam
      </Button>
      <Button
        className="w-1/3"
        type={`${input === "Upload" ? "primary" : "ghost"}`}
        onClick={() => onChangeEnrollMethod("Upload")}
      >
        Upload
      </Button>
    </div>
  )
}
