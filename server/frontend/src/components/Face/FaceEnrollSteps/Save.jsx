import { Button, Image } from "antd"
import { saveFace } from "apis/face"
import { imgSrcToBlob } from "helpers/image"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { clean } from "slices/faceEnroll"

export default function Save({ setCurrent }) {
  const { userid } = useSelector(state => state.auth.user)
  const { croppedFace } = useSelector(state => state.faceEnroll)
  const dispatch = useDispatch()

  const onSave = () => {
    imgSrcToBlob(croppedFace).then(blob => {
      saveFace({ userid, blob }).then(response => {
        dispatch(clean())
        setCurrent(0)
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
