import { Button, Card, Empty, Skeleton, Table } from "antd"
import React, { useEffect, useState } from "react"
import useFetch from "use-http"

const columns = [
    {
        title: "Subject Code",
        dataIndex: "id",
        key: "id",
    },
    {
        title: "Subject Name",
        dataIndex: "name",
        key: "name",
    },
]

export default function Subject({ id }) {
    const [data, setData] = useState(null)
    const { get, response, loading, error } = useFetch(
        "/api/query/user_subject/user"
    )

    useEffect(() => {
        const fetchData = async () => {
            const dataFetched = await get(`/${id}`)
            if (response.ok) {
                setData(dataFetched)
            }
        }
        fetchData()
    }, [id])

    if (error) {
        return <Empty />
    }

    if (loading) {
        return <Skeleton active />
    }

    return (
        <Card
            title='Subjects'
            headStyle={{ fontWeight: "bold" }}
            extra={<Button type='primary'>Add</Button>}
        >
            <Table dataSource={data} columns={columns}></Table>
        </Card>
    )
}
