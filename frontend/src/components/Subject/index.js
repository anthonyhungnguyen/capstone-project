import { Col, Form, Layout, Popconfirm, Row, Table } from "antd"
import Axios from "axios"
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import useFetch from "use-http"
import EditableCell from "./EditableCell"

const { Content } = Layout

const LayoutContent = styled.div`
  background: #fff;
  padding: 24px;
  min-height: 280px;
  margin: 50px 0;
`

export function Subject() {
  const [data, setData] = useState(null)
  const [form] = Form.useForm()
  const [editingKey, setEditingKey] = useState("")
  const { get, post, response, loading, error } = useFetch("/api")

  useEffect(() => {
    const fetchData = async () => {
      const data = await get("/query/subjects")
      if (response.ok) {
        setData(data)
      }
    }
    fetchData()
  }, [])

  const edit = (record) => {
    form.setFieldsValue({
      subjectID: "",
      subjectName: "",
      startTime: "",
      endTime: "",
      weekDay: "",
      ...record,
    })
    setEditingKey(record.key)
  }

  const isEditing = (record) => record.key === editingKey

  const cancel = () => {
    setEditingKey("")
  }

  const save = async (key) => {
    try {
      const row = await form.validateFields()
      const newData = [...data]
      const index = newData.findIndex((item) => key === item.key)

      await Axios.post(`/api/register/subject/timetable/${index}`, row)

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
    {
      title: "Subject Code",
      dataIndex: "subjectID",
      key: "subjectID",
      editable: true,
    },
    {
      title: "Subject Name",
      dataIndex: "subjectName",
      key: "subjectName",
      editable: true,
    },
    {
      title: "Start Time",
      dataIndex: "startTime",
      key: "startTime",
      editable: true,
    },
    {
      title: "End Time",
      dataIndex: "endTime",
      key: "endTime",
      editable: true,
    },
    {
      title: "Week Day",
      dataIndex: "weekDay",
      key: "weekDay",
      editable: true,
    },
    {
      title: "Operation",
      dataIndex: "operation",
      render: (_, record) => {
        const editable = isEditing(record)
        return editable ? (
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
        )
      },
    },
  ]

  const mergedColumns = columns.map((col) => {
    if (!col.editable) {
      return col
    }

    return {
      ...col,
      onCell: (record) => ({
        record,
        inputType: col.dataIndex === "age" ? "number" : "text",
        dataIndex: col.dataIndex,
        title: col.title,
        editing: isEditing(record),
      }),
    }
  })

  return (
    <Content style={{ padding: "0 50px" }}>
      <LayoutContent>
        <Row>
          <Col span={24}>
            <Form form={form} component={false}>
              <Table
                components={{
                  body: {
                    cell: EditableCell,
                  },
                }}
                bordered
                dataSource={data}
                columns={columns}
                columns={mergedColumns}
                rowClassName="editable-row"
                pagination={{
                  onChange: cancel,
                }}
              />
            </Form>
          </Col>
        </Row>
      </LayoutContent>
    </Content>
  )
}
