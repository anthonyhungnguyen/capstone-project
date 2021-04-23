import { Button } from "antd"
import React, { useRef, useCallback } from "react"
import { useDispatch } from "react-redux"
import Webcam from "react-webcam"
import { rawFaceUpdate } from "slices/faceEnroll"

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
}

const WebcamCapture = () => {
  const webcamRef = useRef(null)
  const dispatch = useDispatch()

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot()
    dispatch(rawFaceUpdate(imageSrc))
  }, [webcamRef])

  return (
    <div className="w-full flex items-center justify-between flex-col space-y-4">
      <Webcam
        audio={false}
        height={600}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={600}
        videoConstraints={videoConstraints}
      />
      <Button onClick={capture} type="primary">
        Capture
      </Button>
    </div>
  )
}

export default WebcamCapture
