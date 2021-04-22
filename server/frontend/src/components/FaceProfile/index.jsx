import { Card, Image } from "antd"
import { fetchUserInfo } from "apis/user"
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
    <Card title="Register photos">
      <div className="flex flex-wrap">
        {photos?.map(item => (
          <Image src={item.photo} alt="face_photo" style={{ width: "150px" }} />
        ))}
      </div>
    </Card>
  )
}
