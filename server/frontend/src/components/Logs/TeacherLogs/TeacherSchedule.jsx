import { render } from "@testing-library/react"
import {
  Button,
  Card,
  DatePicker,
  Form,
  Modal,
  Popconfirm,
  Select,
  Table
} from "antd"
import { deleteSchedule, fetchSchedules, updateSchedule } from "apis/register"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import moment from "moment"

export default function TeacherSchedule({ setChosenSchedule }) {
  const [data, setData] = useState(null)
  const { user } = useSelector(state => state.auth)
  const { userid } = user

  const handleOnChange = record => {
    setChosenSchedule(record)
  }

  const columns = [
    { title: "ID", dataIndex: "id", key: "key" },
    {
      title: "Semester",
      dataIndex: "semester"
    },
    {
      title: "Group Code",
      dataIndex: "groupCode"
    },
    {
      title: "Subject ID",
      dataIndex: "subjectID"
    },
    {
      title: "Start Time",
      dataIndex: "startTime",
      render: d => {
        return moment(d).format("YYYY-MM-DD HH:mm:ss")
      }
    },
    {
      title: "End Time",
      dataIndex: "endTime",
      render: d => moment(d).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      title: "Operation",
      dataIndex: "operation",
      render: (_, record) =>
        data.length >= 1 ? (
          <>
            <Button onClick={() => handleOnChange(record)}>View</Button>
          </>
        ) : null
    }
  ]

  useEffect(() => {
    fetchSchedules({ teacherid: userid })
      .then(data => {
        setData(
          data.map(x => {
            return {
              ...x,
              startTime: moment(x.startTime)
                .subtract(7, "hour")
                .format("YYYY-MM-DDTHH:mm:ss"),
              endTime: moment(x.endTime)
                .subtract(7, "hour")
                .format("YYYY-MM-DDTHH:mm:ss")
            }
          })
        )
      })
      .catch(console.error)
  }, [])

  return (
    <Table
      key={"id"}
      loading={data === null}
      dataSource={data}
      columns={columns}
    ></Table>
  )
}
