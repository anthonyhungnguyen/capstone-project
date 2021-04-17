import { fetchFaces, fetchFacesMetadata, getFaces } from "apis/face"
import FaceCard from "components/Face/FaceCard"
import { splitTimestamp } from "helpers/string"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

export default function FaceProfile() {
  const [photos, setPhotos] = useState(null)
  const { userid } = useSelector(state => state.auth.user)

  useEffect(() => {
    const onLoadFacePhotos = async () => {
      const faces = await fetchFaces(userid, "register").then(data => data)
      const metadata = await fetchFacesMetadata(userid, "register").then(
        data => data
      )
      const result = faces.map((f, index) => ({
        photo: f,
        metadata: metadata[index]
      }))
      setPhotos(result)
    }
    onLoadFacePhotos()
  }, [])
  return (
    <MainLayout>
      <div className="space-y-4 flex items-center justify-between">
        {photos?.map(item => (
          <FaceCard photo={item.photo} metadata={item.metadata} />
        ))}
      </div>
    </MainLayout>
  )
}
