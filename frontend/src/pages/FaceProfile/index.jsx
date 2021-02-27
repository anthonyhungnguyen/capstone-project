import { getFaces } from "apis/face"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

export default function FaceProfile() {
  const [photos, setPhotos] = useState(null)
  const { username } = useSelector(state => state.user.userData)

  useEffect(() => {
    const onLoadFacePhotos = async () => {
      await getFaces(username)
        .then(response => {
          setPhotos(response)
        })
        .catch(console.log)
    }
    onLoadFacePhotos()
  }, [])
  console.log(photos)

  return (
    <MainLayout>
      <div className="w-full overflow-y-scroll p-4">
        <div className="w-2/3 m-auto space-y-4 mt-4 border-2 shadow-sm p-5">
          Hello
        </div>
      </div>
    </MainLayout>
  )
}
