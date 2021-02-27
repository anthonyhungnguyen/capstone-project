import WebcamCapture from "components/Webcam"
import MainLayout from "layouts/MainLayout"
import React, { useState } from "react"
import { cropFaceApi, saveFace } from "apis/face"
import { imgSrcToBlob } from "helpers/image"
import { useSelector } from "react-redux"

export default function FaceEnroll() {
  const [enrollMethod, setEnrollMethod] = useState(null)
  const [photoData, setPhotoData] = useState(null)
  const [croppedFace, setCroppedFace] = useState(null)
  const { username } = useSelector(state => state.user.userData)

  const onChangeEnrollMethod = enrollMethod => {
    setEnrollMethod(enrollMethod)
    setPhotoData(null)
  }

  const onVerify = async () => {
    if (photoData) {
      cropFaceApi(photoData).then(croppedFace => {
        setCroppedFace(croppedFace)
      })
    }
  }

  const onSaveFace = async () => {
    if (croppedFace) {
      imgSrcToBlob(croppedFace).then(blob => {
        saveFace({ username, blob }).then(response => {
          console.log(response)
        })
      })
    }
  }

  return (
    <MainLayout>
      <div className="w-full overflow-y-scroll p-4">
        <div className="w-2/3 m-auto space-y-4 mt-4">
          <p className="text-lg font-bold text-gray-700">
            1. Choose enroll method
          </p>
          <div className="flex items-center justify-center space-x-5">
            <button
              className="p-2 border-2 rounded-md shadow-md font-bold w-1/3"
              onClick={() => onChangeEnrollMethod("Webcam")}
            >
              Webcam
            </button>
            <button
              className="p-2 border-2 rounded-md shadow-md font-bold w-1/3"
              onClick={() => onChangeEnrollMethod("Upload")}
            >
              Upload
            </button>
          </div>
          {enrollMethod && (
            <div>
              <p className="text-lg font-bold text-gray-700">
                2. {enrollMethod}
              </p>
              {enrollMethod === "Webcam" ? (
                <WebcamCapture setPhotoData={setPhotoData} />
              ) : null}
            </div>
          )}
          {photoData && (
            <div className="space-y-4 flex items-center justify-center flex-col">
              <p className="text-lg font-bold text-gray-700">3. Verify</p>

              <img
                src={photoData}
                alt="verify_photo"
                style={{ height: "350px" }}
              />
              <button
                className="w-full border-2 p-2 font-bold shadow-md"
                onClick={onVerify}
              >
                Send
              </button>
            </div>
          )}
          {croppedFace && (
            <div className="space-y-4 flex items-center justify-center flex-col">
              <p className="text-lg font-bold text-gray-700">4. Result</p>
              <img src={croppedFace} alt="cropped_face" />
              <button
                onClick={onSaveFace}
                className="w-full border-2 p-2 font-bold shadow-md"
              >
                Save
              </button>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  )
}
