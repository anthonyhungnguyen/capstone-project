import {
  Button,
  Card,
  Checkbox,
  DatePicker,
  Form,
  Input,
  message,
  Select,
  TimePicker
} from "antd"
import { testPublishTopic } from "apis/register"
import { findAllSubjects } from "apis/subject"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

const { Option } = Select
const { RangePicker } = DatePicker

export default function TeacherRegister() {
  const [subjects, setSubjects] = useState(null)
  const { user } = useSelector(state => state.auth)
  const { userid } = user

  useEffect(() => {
    findAllSubjects().then(setSubjects)
  }, [])

  const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 14 }
  }
  const tailLayout = {
    wrapperCol: { offset: 8, span: 16 }
  }

  const onFinish = values => {
    const sentData = {
      ...values,
      teacherID: userid,
      startTime: values.startEndTime[0].format("YYYY-MM-DD HH:mm:ss"),
      endTime: values.startEndTime[1].format("YYYY-MM-DD HH:mm:ss")
    }
    delete sentData["startEndTime"]
    testPublishTopic(sentData).then(result => message.info(result))
  }

  const onFinishFailed = errorInfo => {
    console.log("Failed:", errorInfo)
  }

  return (
    <>
      <Card className="w-2/3" title="Registration form">
        <Form
          {...layout}
          name="basic"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
        >
          <Form.Item
            label="Semester"
            name="semester"
            // rules={[{ required: true, message: "Please input semester!" }]}
          >
            <Select>
              <Option value="201">201</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Group Code"
            name="groupCode"
            rules={[{ required: true, message: "Please input group code!" }]}
          >
            <Select>
              {subjects &&
                [
                  ...new Set(subjects.map(s => s["subjectIDDto"]["groupCode"]))
                ].map((id, index) => (
                  <Option key={index} value={id}>
                    {id}
                  </Option>
                ))}
            </Select>
          </Form.Item>

          <Form.Item
            label="Subject ID"
            name="subjectID"
            rules={[{ required: true, message: "Please input subject ID!" }]}
          >
            <Select>
              {subjects &&
                [...new Set(subjects.map(s => s["subjectIDDto"]["id"]))].map(
                  (id, index) => (
                    <Option key={index} value={id}>
                      {id}
                    </Option>
                  )
                )}
            </Select>
          </Form.Item>

          <Form.Item
            label="Start - End time"
            name="startEndTime"
            rules={[
              { required: true, message: "Please input start - end time!" }
            ]}
          >
            <RangePicker showTime />
          </Form.Item>

          <Form.Item
            label="Device ID"
            name="deviceID"
            // rules={[{ required: true, message: "Please input device id!" }]}
          >
            <Select>
              <Option value="1">1</Option>
            </Select>
          </Form.Item>

          <Form.Item {...tailLayout}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </>
  )
}
