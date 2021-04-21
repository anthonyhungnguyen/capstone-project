import { fetchFaces, fetchFacesMetadata, getFaces } from "apis/face"
import { fetchUserInfo, fetchUsersInfo } from "apis/user"
import FaceCard from "components/FaceCard"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

export default function FaceProfile() {
  const [photos, setPhotos] = useState(null)
  const { userid } = useSelector(state => state.auth.user)

  useEffect(() => {
    const onLoadFacePhotos = async () => {
      await fetchUserInfo(userid).then(data => {
        const photosToInsert = data.registers.map(p => ({
          photo: p.imageLink
        }))
        setPhotos(photosToInsert)
      })
    }
    onLoadFacePhotos()
  }, [])
  return (
    <MainLayout>
      <div className="space-y-4 flex items-center justify-between">
        {photos?.map(item => (
          <FaceCard photo={item.photo} />
        ))}
      </div>
    </MainLayout>
  )
}
