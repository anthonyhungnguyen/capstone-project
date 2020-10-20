import { Card, Empty, Skeleton, Table } from "antd"
import dayjs from "dayjs"
import React, { useEffect, useState } from "react"
import useFetch from "use-http"

const columns = [
  {
    title: "Subject Code",
    dataIndex: "subjectID",
    key: "subjectID",
  },
  {
    title: "Type",
    dataIndex: "type",
    key: "type",
  },
  {
    title: "When",
    dataIndex: "timestamp",
    key: "timestamp",
    render: (timestamp) => dayjs(timestamp).format("YYYY-MM-DD HH:mm:ss"),
  },
]

export default function Log({ id }) {
  const [data, setData] = useState(null)
  const { get, response, loading, error } = useFetch("/api/query/user")

  useEffect(() => {
    const fetchData = async () => {
      const dataFetched = await get(`/${id}/log`)
      if (response.ok) {
        setData(dataFetched)
      }
    }
    fetchData()
  }, [id])

  if (error) {
    return <Empty />
  }

  if (loading) {
    return <Skeleton active />
  }
  return (
    <Card title="Logs" headStyle={{ fontWeight: "bold" }}>
      <Table dataSource={data} columns={columns}></Table>
    </Card>
  )
}
