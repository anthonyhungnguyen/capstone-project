import React, { useRef, useCallback } from "react"
import Webcam from "react-webcam"

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user"
}

const WebcamCapture = ({ setPhotoData }) => {
  const webcamRef = useRef(null)

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot()
    setPhotoData(imageSrc)
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
      <button
        onClick={capture}
        className="w-full border-2 p-2 font-bold shadow-md"
      >
        Capture
      </button>
    </div>
  )
}

export default WebcamCapture
