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
    TimePicker,
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
            const data = await get("/query/timetable")
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

    const del = async (key) => {
        try {
            const row = await form.validateFields()
            const newData = [...data]
            const index = newData.findIndex((item) => key === item.key)

            if (index > -1) {
                await Axios.delete(
                    `/api/remove/timetable/${newData[index].key}`
                )
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

    const handleModelOkay = () => {
        setModalVisible(false)
    }

    const handleModelCancel = () => {
        setModalVisible(false)
    }

    const handleAddFinish = async (values) => {
        values = {
            ...values,
            start_time: values.time_range[0].format("hh:mm:ss"),
            end_time: values.time_range[1].format("hh:mm:ss"),
            subject: {
                id: values.subject_id,
            },
        }
        delete values["time_range"]
        delete values["subject_id"]
        await Axios.post("api/register/timetable", values)
            .then(() => {
                message.success("Insert successfully")
            })
            .catch((err) => message.error(err))
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
                        name='subject_id'
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
                        label='Time Range'
                        name='time_range'
                        rules={[
                            {
                                required: true,
                                message: "Please input start time",
                            },
                        ]}
                    >
                        <RangePicker />
                    </Form.Item>

                    <Form.Item
                        label='Day In Week'
                        name='day_in_week'
                        rules={[
                            {
                                required: true,
                                message: "Please input day in week",
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
                title='Timetable'
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
                        columns={mergedColumns}
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
