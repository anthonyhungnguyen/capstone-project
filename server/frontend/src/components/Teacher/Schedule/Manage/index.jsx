import { Button, DatePicker, Form, Modal, Table } from "antd"
import { deleteSchedule, fetchSchedules, updateSchedule } from "apis/register"
import moment from "moment"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

const { RangePicker } = DatePicker

export default function TeacherManage({ subject }) {
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

  const handleOnChange = record => {
    setEditting(true)
    setCurrentEdittingRecord(record)
  }

  const handleDelete = record => {
    deleteSchedule(record)
  }

  const columns = [
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
            <Button
              onClick={() => handleOnChange(record)}
              disabled={moment(record.endTime).isBefore(
                moment.utc().add(7, "hours")
              )}
            >
              Change
            </Button>
            <Button
              onClick={() => handleDelete(record)}
              disabled={moment(record.endTime).isBefore(
                moment.utc().add(7, "hours")
              )}
            >
              Delete
            </Button>
          </>
        ) : null
    }
  ]

  useEffect(() => {
    fetchSchedules({ teacherid: userid }).then(data => {
      const { id, groupCode, semester } = subject
      setData(
        data.filter(
          d =>
            d.subjectID === id &&
            d.groupCode === groupCode &&
            d.semester === semester
        )
      )
    })
  }, [userid, subject])

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
        style={{ width: "100%" }}
      ></Table>
    </>
  )
}
