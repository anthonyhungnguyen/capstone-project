import { Button, Card, Select, Table } from "antd"
import React, { useEffect, useState } from "react"
import Axios from "axios"

const { Option } = Select

const columns = [
    {
        title: "Code",
        dataIndex: "id",
        key: "id",
        fixed: "left",
        width: 100,
    },
    {
        title: "Name",
        dataIndex: "name",
        key: "name",
        fixed: "left",
        width: 100,
    },
    {
        title: "Group",
        dataIndex: "groupCode",
        key: "groupCode",
        width: 100,
    },

    {
        title: "Semester",
        dataIndex: "semester",
        key: "semester",
        width: 100,
    },
    {
        title: "Week Day",
        dataIndex: "weekDay",
        key: "week_day",
        width: 100,
    },
    {
        title: "Time Range",
        dataIndex: "timeRange",
        key: "timeRange",
        width: 200,
    },
    {
        title: "Room",
        dataIndex: "room",
        key: "room",
        width: 100,
    },
    {
        title: "Base",
        dataIndex: "base",
        key: "base",
        width: 100,
    },
    {
        title: "Week Learn",
        dataIndex: "weekLearn",
        key: "weekLearn",
        width: 300,
    },
]

export default function Subject({ id }) {
    const [data, setData] = useState(null)

    useEffect(() => {
        Axios.get(`api/query/user/${id}/${201}/enrollment`)
            .then((response) => setData(response.data))
            .catch(console.err)
    }, [id])
    return (
        <Card
            title='Subject'
            headStyle={{ fontWeight: "bold" }}
            extra={
                <>
                    {/* # TODO: Add Semester Selection */}
                    <Button type='primary'>Add</Button>
                </>
            }
        >
            <Table
                dataSource={data}
                columns={columns}
                scroll={{ y: 500 }}
                sticky
            ></Table>
        </Card>
    )
}
