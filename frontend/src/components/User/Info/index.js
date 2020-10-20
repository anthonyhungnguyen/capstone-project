import { Card, Descriptions, Empty, Image, Skeleton } from "antd"
import dayjs from "dayjs"
import React, { useEffect, useState } from "react"
import useFetch from "use-http"

export default function Info({ id }) {
  const [userInfo, setUserInfo] = useState(null)
  const { get, response, loading, error } = useFetch("api/query/user")

  useEffect(() => {
    const fetchUserOnMount = async () => {
      const userData = await get(`/${id}`)
      if (response.ok) {
        setUserInfo(userData)
      }
    }
    fetchUserOnMount()
  }, [id])

  if (error) {
    return <Empty />
  }

  if (loading) {
    return <Skeleton active />
  }

  return (
    <Card title="Subjects" headStyle={{ fontWeight: "bold" }}>
      <Descriptions bordered>
        <Descriptions.Item label="ID">{userInfo?.["id"]}</Descriptions.Item>
        <Descriptions.Item label="Name">{userInfo?.["name"]}</Descriptions.Item>
        <Descriptions.Item label="Register At">
          {dayjs(userInfo?.["register_at"]).format("YYYY-MM-DD HH:mm:ss")}
        </Descriptions.Item>
        <Descriptions.Item label="Updated At">
          {dayjs(userInfo?.["update_at"]).format("YYYY-MM-DD HH:mm:ss")}
        </Descriptions.Item>
        <Descriptions.Item label="Avatar">
          <Image src={userInfo?.["image_link"]} width={100} />
        </Descriptions.Item>
      </Descriptions>
    </Card>
  )
}
