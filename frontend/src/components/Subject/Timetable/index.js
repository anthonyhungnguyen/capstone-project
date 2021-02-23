import {
  Button,
  Card,
  Col,
  Form,
  Input,
  Layout,
  message,
  Popconfirm,
  Table,
  TimePicker
} from "antd"
import Modal from "antd/lib/modal/Modal"
import Axios from "axios"
import React, { useEffect, useState } from "react"
import useFetch from "use-http"
import EditableCell from "../EditableCell"

const { RangePicker } = TimePicker

export default function Timetable() {
  const [data, setData] = useState(null)
  const [form] = Form.useForm()
  const [editingKey, setEditingKey] = useState("")
  const [modalVisible, setModalVisible] = useState(false)
  const { get, post, response, loading, error } = useFetch("/api")

  useEffect(() => {
    const fetchData = async () => {
      const data = await get(`/query/subjects/${201}`)
      if (response.ok) {
        setData(data.map((x, i) => ({ key: i.toString(), ...x })))
      }
    }
    fetchData()
  }, [get, response.ok])

  const edit = record => {
    form.setFieldsValue({
      id: "",
      name: "",
      groupCode: "",
      semester: "",
      timeRange: "",
      weekDay: "",
      base: "",
      weekLearn: "",
      ...record
    })
    setEditingKey(record.key)
  }

  const isEditing = record => record.key === editingKey

  const cancel = () => {
    setEditingKey("")
  }

  const del = async key => {
    try {
      const row = await form.validateFields()
      const newData = [...data]
      const index = newData.findIndex(item => key === item.key)

      if (index > -1) {
        await Axios.delete(`/api/remove/timetable/${newData[index].key}`)
        newData.splice(index, 1)
        setData(newData)
        setEditingKey("")

        message.success("Delete successfully")
      } else {
        newData.push(row)
        setData(newData)
        setEditingKey("")
      }
    } catch (errInfo) {
      console.log("Validate Failed:", errInfo)
      message.error("Delete failed")
    }
  }

  const save = async key => {
    try {
      const row = await form.validateFields()
      const newData = [...data]
      const index = newData.findIndex(item => key === item.key)
      await Axios.put(
        `/api/update/subject/timetable/${newData[index].key}`,
        row
      )

      if (index > -1) {
        const item = newData[index]
        newData.splice(index, 1, { ...item, ...row })
        setData(newData)
        setEditingKey("")
      } else {
        newData.push(row)
        setData(newData)
        setEditingKey("")
      }
    } catch (errInfo) {
      console.log("Validate Failed:", errInfo)
    }
  }

  const columns = [
    { title: "Index", dataIndex: "key", key: "key" },
    {
      title: "Code",
      dataIndex: "id",
      key: "id",
      fixed: "left",
      editable: true
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      fixed: "left",
      editable: true
    },
    {
      title: "Group",
      dataIndex: "groupCode",
      key: "groupCode",
      editable: true
    },

    {
      title: "Semester",
      dataIndex: "semester",
      key: "semester",
      editable: true
    },
    {
      title: "Week Day",
      dataIndex: "weekDay",
      key: "week_day",
      editable: true
    },
    {
      title: "Time Range",
      dataIndex: "timeRange",
      key: "timeRange",
      editable: true
    },
    {
      title: "Room",
      dataIndex: "room",
      key: "room",
      editable: true
    },
    {
      title: "Base",
      dataIndex: "base",
      key: "base",
      editable: true
    },
    {
      title: "Week Learn",
      dataIndex: "weekLearn",
      key: "weekLearn",
      editable: true
    },
    {
      title: "Operation",
      dataIndex: "operation",
      fixed: "right",
      render: (_, record) => {
        const editable = isEditing(record)
        return (
          <>
            {editable ? (
              <span>
                <a
                  href="javascript:;"
                  onClick={() => save(record.key)}
                  style={{ marginRight: 8 }}
                >
                  Save
                </a>
                <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                  <a>Cancel</a>
                </Popconfirm>
              </span>
            ) : (
              <a disabled={editingKey !== ""} onClick={() => edit(record)}>
                Edit
              </a>
            )}
            <span style={{ marginLeft: "5px" }}>
              <a href="javascript:;" onClick={() => del(record.key)}>
                Delete
              </a>
            </span>
          </>
        )
      }
    }
  ]

  const mergedColumns = columns.map(col => {
    if (!col.editable) {
      return col
    }

    return {
      ...col,
      onCell: record => ({
        record,
        inputType: col.dataIndex === "age" ? "number" : "text",
        dataIndex: col.dataIndex,
        title: col.title,
        editing: isEditing(record)
      })
    }
  })

  const handleModelOkay = () => {
    setModalVisible(false)
  }

  const handleModelCancel = () => {
    setModalVisible(false)
  }

  const handleAddFinish = async values => {
    values = {
      ...values,
      start_time: values.time_range[0].format("hh:mm:ss"),
      end_time: values.time_range[1].format("hh:mm:ss"),
      subject: {
        id: values.subject_id
      }
    }
    delete values["time_range"]
    delete values["subject_id"]
    await Axios.post("api/register/timetable", values)
      .then(() => {
        message.success("Insert successfully")
      })
      .catch(err => message.error(err))
  }
  return (
    <>
      <Modal
        title="Add New Timetable"
        visible={modalVisible}
        onOk={handleModelOkay}
        onCancel={handleModelCancel}
      >
        <Form
          onFinish={handleAddFinish}
          labelCol={{ span: 8 }}
          wrapperCol={{ span: 16 }}
        >
          <Form.Item
            label="Code"
            name="id"
            rules={[
              {
                required: true,
                message: "Please input subject id"
              }
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Name"
            name="name"
            rules={[
              {
                required: true,
                message: "Please input subject id"
              }
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Group"
            name="groupCode"
            rules={[
              {
                required: true,
                message: "Please input start time"
              }
            ]}
          >
            <RangePicker />
          </Form.Item>

          <Form.Item
            label="Semester"
            name="semester"
            rules={[
              {
                required: true,
                message: "Please input day in week"
              }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Time Range"
            name="timeRange"
            rules={[
              {
                required: true,
                message: "Please input day in week"
              }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Room"
            name="room"
            rules={[
              {
                required: true,
                message: "Please input day in week"
              }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Base"
            name="base"
            rules={[
              {
                required: true,
                message: "Please input day in week"
              }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Week Learn"
            name="weekLearn"
            rules={[
              {
                required: true,
                message: "Please input day in week"
              }
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
            <Button type="primary" htmlType="submit">
              Submit
            </Button>
          </Form.Item>
        </Form>
      </Modal>
      <Card
        title="Timetable"
        headStyle={{ fontWeight: "bold" }}
        extra={
          <Button type="primary" onClick={() => setModalVisible(old => !old)}>
            Add
          </Button>
        }
      >
        <Form form={form} component={false}>
          <Table
            components={{
              body: {
                cell: EditableCell
              }
            }}
            bordered
            dataSource={data}
            columns={columns}
            columns={mergedColumns}
            rowClassName="editable-row"
            pagination={{
              onChange: cancel
            }}
          />
        </Form>
      </Card>
    </>
  )
}
