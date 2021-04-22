import { Image, Table } from "antd"
import { fetchLogsStudent } from "apis/attendance"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import moment from "moment"

export default function StudentLogs() {
  const { logs } = useSelector(state => state.log)
  const columns = [
    {
      title: "Subject ID",
      dataIndex: "subjectID",
      key: "subjectID",
      filters: [...new Set(logs?.map(x => x.subjectID))].map(x => ({
        text: x,
        value: x
      })),
      onFilter: (value, record) => record.subjectID === value
    },
    {
      title: "Group Code",
      dataIndex: "groupCode",
      key: "groupCode",
      filters: [...new Set(logs?.map(x => x.groupCode))].map(x => ({
        text: x,
        value: x
      })),
      onFilter: (value, record) => record.groupCode === value
    },
    {
      title: "At",
      dataIndex: "timestamp",
      key: "timestamp",
      render: d => {
        return moment(d.split("+")[0]).format("yyyy-MM-DD hh:mm:ss")
      }
    },
    {
      title: "Photo",
      dataIndex: "photo",
      key: "photo",
      render: d => <Image src={d} alt="attendance" style={{ width: "120px" }} />
    }
  ]
  return <Table dataSource={logs} columns={columns} loading={logs === null} />
}
