import { Button, Image } from "antd"
import { saveFace } from "apis/face"
import { imgSrcToBlob } from "helpers/image"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { clean } from "slices/faceEnroll"

export default function Save({ setCurrent }) {
  const { username } = useSelector(state => state.user.userData)
  const { croppedFace } = useSelector(state => state.faceEnroll)
  const dispatch = useDispatch()

  const onSave = () => {
    imgSrcToBlob(croppedFace).then(blob => {
      saveFace({ username, blob }).then(response => {
        dispatch(clean())
        setCurrent(0)
        console.log(response)
      })
    })
  }

  return croppedFace ? (
    <div className="flex items-center justify-between flex-col space-y-4">
      <Image src={croppedFace} alt="cropped_face" width={300} />
      <Button onClick={onSave} type="primary">
        Save
      </Button>
    </div>
  ) : null
}
