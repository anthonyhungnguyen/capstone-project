import { Button, Image } from "antd"
import { cropFaceApi } from "apis/face"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { croppedFaceUpdate } from "slices/faceEnroll"

export default function Verify() {
  const { rawFace } = useSelector(state => state.faceEnroll)
  const dispatch = useDispatch()
  const onVerify = async () => {
    cropFaceApi(rawFace).then(croppedFace => {
      dispatch(croppedFaceUpdate(croppedFace))
    })
  }
  return rawFace ? (
    <div className="flex items-center justify-between flex-col space-y-4">
      <Image src={rawFace} alt="raw_face" />
      <Button onClick={onVerify} type="primary">
        Send
      </Button>
    </div>
  ) : null
}
