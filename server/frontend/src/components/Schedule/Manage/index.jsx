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

const { Option } = Select
const { RangePicker } = DatePicker

export default function TeacherManage() {
  const [data, setData] = useState(null)
  const [editting, setEditting] = useState(false)
  const [currentEdittingRecord, setCurrentEdittingRecord] = useState(null)
  const { user } = useSelector(state => state.auth)
  const { userid } = user

  const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 14 }
  }
  const tailLayout = {
    wrapperCol: { offset: 8, span: 16 }
  }

  const onFinish = values => {
    const updateSchduleData = {
      ...currentEdittingRecord,
      startTime: values.startEndTime[0].format("YYYY-MM-DD HH:mm:ss"),
      endTime: values.startEndTime[1].format("YYYY-MM-DD HH:mm:ss")
    }
    updateSchedule(updateSchduleData)
  }

  const onFinishFailed = errorInfo => {
    console.log("Failed:", errorInfo)
  }

  const handleOnChange = record => {
    setEditting(true)
    setCurrentEdittingRecord(record)
  }

  const handleDelete = record => {
    deleteSchedule(record)
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
      render: d => moment(d).format("YYYY-MM-DD HH:mm:ss")
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
            <Button onClick={() => handleOnChange(record)}>Change</Button>
            <Button onClick={() => handleDelete(record)}>Delete</Button>
          </>
        ) : null
    }
  ]

  useEffect(() => {
    fetchSchedules({ teacherid: userid })
      .then(data => {
        setData(data)
      })
      .catch(console.error)
  }, [])

  return (
    <>
      <Modal
        title="Change"
        visible={editting}
        onCancel={() => setEditting(false)}
        onOk={() => setEditting(false)}
        width={700}
      >
        <Form
          {...layout}
          name="basic"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item
            label="Start - End time"
            name="startEndTime"
            rules={[
              { required: true, message: "Please input start - end time!" }
            ]}
          >
            <RangePicker
              defaultValue={[
                moment(currentEdittingRecord?.startTime),
                moment(currentEdittingRecord?.endTime)
              ]}
              showTime
            />
          </Form.Item>

          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Modal>
      <Table
        key={"id"}
        loading={data === null}
        dataSource={data}
        columns={columns}
      ></Table>
    </>
  )
}
