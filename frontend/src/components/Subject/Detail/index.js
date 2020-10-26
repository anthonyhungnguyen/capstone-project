import { Button, Card, Form, Input, message, Popconfirm, Table } from "antd"
import Modal from "antd/lib/modal/Modal"
import Axios from "axios"
import React, { useEffect, useState } from "react"
import styled from "styled-components"
import useFetch from "use-http"
import EditableCell from "../EditableCell"

export default function Detail() {
    const [data, setData] = useState(null)
    const [form] = Form.useForm()
    const [editingKey, setEditingKey] = useState("")
    const [modalVisible, setModalVisible] = useState(false)
    const { get, post, response, loading, error } = useFetch("/api")

    useEffect(() => {
        Axios.get("api/query/subject")
            .then((response) => setData(response.data))
            .catch(console.err)
    }, [])

    const edit = (record) => {
        form.setFieldsValue({
            id: "",
            name: "",
            ...record,
        })
        setEditingKey(record.key)
    }

    const isEditing = (record) => record.key === editingKey

    const cancel = () => {
        setEditingKey("")
    }

    const del = async (key) => {
        try {
            const row = await form.validateFields()
            const newData = [...data]
            const index = newData.findIndex((item) => key === item.key)

            if (index > -1) {
                await Axios.delete(`/api/remove/subject/${newData[index].id}`)
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

    const save = async (key) => {
        try {
            const row = await form.validateFields()
            const newData = [...data]
            const index = newData.findIndex((item) => key === item.key)
            // await Axios.post(
            //     `/api/register/subject/timetable/${newData[index].key}`,
            //     row
            // )

            if (index > -1) {
                const item = newData[index]
                newData.splice(index, 1, { ...item, ...row })
                setData(newData)
                setEditingKey("")
                message.success("Update successfully")
            } else {
                newData.push(row)
                setData(newData)
                setEditingKey("")
            }
        } catch (errInfo) {
            console.log("Validate Failed:", errInfo)
            message.error("Update failed")
        }
    }

    const columns = [
        {
            title: "Subject Code",
            dataIndex: "id",
            key: "id",
            editable: true,
        },
        {
            title: "Subject Name",
            dataIndex: "name",
            key: "name",
            editable: true,
        },
        {
            title: "Operation",
            dataIndex: "operation",
            render: (_, record) => {
                const editable = isEditing(record)
                return (
                    <>
                        {editable ? (
                            <span>
                                <a
                                    href='javascript:;'
                                    onClick={() => save(record.key)}
                                    style={{ marginRight: 8 }}
                                >
                                    Save
                                </a>
                                <Popconfirm
                                    title='Sure to cancel?'
                                    onConfirm={cancel}
                                >
                                    <a>Cancel</a>
                                </Popconfirm>
                            </span>
                        ) : (
                            <a
                                disabled={editingKey !== ""}
                                onClick={() => edit(record)}
                            >
                                Edit
                            </a>
                        )}
                        <span style={{ marginLeft: "5px" }}>
                            <a
                                href='javascript:;'
                                onClick={() => del(record.key)}
                            >
                                Delete
                            </a>
                        </span>
                    </>
                )
            },
        },
    ]

    const handleModelOkay = () => {
        setModalVisible(false)
    }

    const handleModelCancel = () => {
        setModalVisible(false)
    }

    const handleAddFinish = async (values) => {
        await post("/register/subject", values)
        if (response.ok) {
            message.success("Insert successfully")
        } else {
            message.error("Insert Fail")
        }
    }
    return (
        <>
            <Modal
                title='Add New Timetable'
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
                        label='Subject ID'
                        name='id'
                        rules={[
                            {
                                required: true,
                                message: "Please input subject id",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        label='Subject Name'
                        name='name'
                        rules={[
                            {
                                required: true,
                                message: "Please input subject name",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button type='primary' htmlType='submit'>
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
            <Card
                title='Subject'
                headStyle={{ fontWeight: "bold" }}
                extra={
                    <Button
                        type='primary'
                        onClick={() => setModalVisible((old) => !old)}
                    >
                        Add
                    </Button>
                }
            >
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
                        rowClassName='editable-row'
                        pagination={{
                            onChange: cancel,
                        }}
                    />
                </Form>
            </Card>
        </>
    )
}
