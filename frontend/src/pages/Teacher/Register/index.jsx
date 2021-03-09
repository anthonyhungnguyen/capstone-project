import { Button, Card, Checkbox, Form, Input, Select, TimePicker } from "antd"
import { testPublishTopic } from "apis/register"
import { findAllSubjects } from "apis/subject"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"

const { Option } = Select

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
      startTime: values.startEndTime[0].format("hh:mm"),
      endTime: values.startEndTime[1].format("hh:mm")
    }
    delete sentData["startEndTime"]
    testPublishTopic(sentData)
  }

  const onFinishFailed = errorInfo => {
    console.log("Failed:", errorInfo)
  }

  return (
    <MainLayout>
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
            <TimePicker.RangePicker order />
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
    </MainLayout>
  )
}
