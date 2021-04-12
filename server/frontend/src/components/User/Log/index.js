import { Card, Empty, Skeleton, Table } from "antd"
import dayjs from "dayjs"
import React, { useEffect, useState } from "react"
import axios from "axios"
import moment from "moment"
const columns = [
  {
    title: "Semester",
    dataIndex: "semester"
  },
  {
    title: "Group Code",
    dataIndex: "groupCode"
  },
  {
    title: "Subject Code",
    dataIndex: "subjectID"
  },
  {
    title: "Type",
    dataIndex: "type"
  },
  {
    title: "When",
    dataIndex: "timestamp",
    key: "timestamp",
    render: timestamp => dayjs(timestamp).format("YYYY-MM-DD HH:mm:ss")
  }
]

export default function Log({ id }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    axios
      .get(`/api/query/user/${id}/logs`)
      .then(res =>
        setData(
          res.data.sort((a, b) => moment(b.timstamp) - moment(a.timestamp))
        )
      )
      .catch(console.error)
  }, [id])
  return (
    <Card title="Logs" headStyle={{ fontWeight: "bold" }}>
      <Table dataSource={data} columns={columns}></Table>
    </Card>
  )
}
