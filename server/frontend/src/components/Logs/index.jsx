import { Table } from "antd"
import React from "react"

export default function Logs() {
  const dataSource = [
    {
      key: "1",
      semester: "201",
      subjectID: "CO3066",
      groupCode: "CC01",
      type: "Late",
      timestamp: "28/01/2021 16:50"
    },
    {
      key: "1",
      semester: "201",
      subjectID: "CO3067",
      groupCode: "CC01",
      type: "On-time",
      timestamp: "27/01/2021 14:50"
    },
    {
      key: "1",
      semester: "201",
      subjectID: "CO4027",
      groupCode: "CC01",
      type: "Miss",
      timestamp: "27/01/2021 17:50"
    }
  ]
  const columns = [
    { title: "Semester", dataIndex: "semester", key: "semester" },
    {
      title: "Subject ID",
      dataIndex: "subjectID",
      key: "subjectID"
    },
    {
      title: "Group Code",
      dataIndex: "groupCode",
      key: "groupCode"
    },
    {
      title: "Type",
      dataIndex: "type",
      key: "type"
    },
    {
      title: "At",
      dataIndex: "timestamp",
      key: "timestamp"
    }
  ]
  return <Table dataSource={dataSource} columns={columns} />
}
