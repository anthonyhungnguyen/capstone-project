import { Card, Image } from "antd"
import { fetchUserInfo } from "apis/user"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

export default function FaceProfile() {
  const { registers } = useSelector(state => state.user)

  return (
    <Card title="Register photos">
      <div className="flex flex-wrap">
        {registers?.map(item => (
          <Image
            src={item.imageLink}
            alt="face_photo"
            style={{ width: "150px" }}
          />
        ))}
      </div>
    </Card>
  )
}
