import { Button, Card, DatePicker, Form, Input, message, Select } from "antd"
import { testPublishTopic } from "apis/register"
import React from "react"
import { useSelector } from "react-redux"

const { Option } = Select
const { RangePicker } = DatePicker

export default function TeacherRegister({ subject }) {
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
    const sentData = {
      ...values,
      subjectID: subject.id,
      groupCode: subject.groupCode,
      semester: subject.semester,
      teacherID: userid,
      startTime: values.startEndTime[0].format("YYYY-MM-DD HH:mm:ss"),
      endTime: values.startEndTime[1].format("YYYY-MM-DD HH:mm:ss")
    }
    delete sentData["startEndTime"]
    testPublishTopic(sentData).then(result => message.info(result))
  }

  return (
    <>
      <Card
        className="w-2/3"
        title={`Registration form | ${subject?.id} - ${subject?.groupCode}`}
      >
        <Form {...layout} name="basic" onFinish={onFinish}>
          <Form.Item
            label="Start - End time"
            name="startEndTime"
            rules={[
              { required: true, message: "Please input start - end time!" }
            ]}
          >
            <RangePicker showTime />
          </Form.Item>

          <Form.Item label="Device ID" name="deviceID">
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
