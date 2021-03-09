import { getFaces } from "apis/face"
import FaceCard from "components/Face/FaceCard"
import { splitTimestamp } from "helpers/string"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

export default function FaceProfile() {
  const [photos, setPhotos] = useState(null)
  const { username } = useSelector(state => state.auth.user)

  useEffect(() => {
    const onLoadFacePhotos = async () => {
      await getFaces(username)
        .then(response => {
          setPhotos(processResponse(response))
        })
        .catch(console.log)
    }
    const processResponse = data => {
      return data.map(d => ({
        base64: `data:image/jpeg;base64,${d.photo.data}`,
        timestamp: splitTimestamp(d.timestamp),
        status: d.status
      }))
    }
    onLoadFacePhotos()
  }, [])

  return (
    <MainLayout>
      <div className="space-y-4 flex items-center justify-between">
        {photos?.map(photo => (
          <FaceCard photo={photo} />
        ))}
      </div>
    </MainLayout>
  )
}
