import { Card, Col, Row } from "antd"
import React, { useEffect, useState } from "react"
import Axios from "axios"
export default function Info({ id }) {
    const [userInfo, setUserInfo] = useState(null)

    useEffect(() => {
        Axios.get(`api/query/user/${id}`)
            .then((response) => setUserInfo(response.data))
            .catch(console.err)
    }, [id])
    return (
        <Card title='Identity' headStyle={{ fontWeight: "bold" }}>
            <Row gutter={[12, 12]}>
                <Col span={12} className='font-bold'>
                    Avatar
                </Col>
                <Col span={12}>{userInfo?.["image_url"]}</Col>
            </Row>
            <Row gutter={[12, 12]}>
                <Col span={12} className='font-bold'>
                    ID
                </Col>
                <Col span={12}>{userInfo?.["id"]}</Col>
            </Row>
            <Row gutter={[12, 12]}>
                <Col span={12} className='font-bold'>
                    Name
                </Col>
                <Col span={12}>{userInfo?.["name"]}</Col>
            </Row>
            <Row gutter={[12, 12]}>
                <Col span={12} className='font-bold'>
                    Gender
                </Col>
                <Col span={12}>{userInfo?.["gender"]}</Col>
            </Row>
            <Row gutter={[12, 12]}>
                <Col span={12} className='font-bold'>
                    Major Code
                </Col>
                <Col span={12}>{userInfo?.["majorCode"]}</Col>
            </Row>
        </Card>
    )
}
