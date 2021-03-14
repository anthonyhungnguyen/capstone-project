import { Button, Card, Select, Table } from "antd"
import React, { useEffect, useState } from "react"
import { findAllSubjectsEnrolledByUser } from "apis/enrollment"

const { Option } = Select

const columns = [
  {
    title: "Code",
    dataIndex: "id",
    key: "id",
    fixed: "left",
    width: 100
  },
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
    fixed: "left",
    width: 100
  },
  {
    title: "Group",
    dataIndex: "groupCode",
    key: "groupCode",
    width: 100
  },
  {
    title: "Semester",
    dataIndex: "semester",
    key: "semester",
    width: 100
  }
]

export default function Subject({ id }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    findAllSubjectsEnrolledByUser().then(setData)
  }, [id])
  return (
    <Card
      title="Subject"
      headStyle={{ fontWeight: "bold" }}
      extra={
        <>
          {/* # TODO: Add Semester Selection */}
          <Button type="primary">Add</Button>
        </>
      }
    >
      <Table
        dataSource={data}
        columns={columns}
        scroll={{ y: 500 }}
        sticky
      ></Table>
    </Card>
  )
}
