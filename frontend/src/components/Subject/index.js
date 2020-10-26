import { Col, Layout, Row } from "antd"
import React from "react"
import Detail from "./Detail"
import Timetable from "./Timetable"
const { Content } = Layout

export default function Subject() {
    return (
        <Content style={{ padding: "20px 50px" }}>
            <Row gutter={[12, 12]}>
                <Col span={24}>
                    <Timetable />
                </Col>
                <Col span={24}>
                    <Detail />
                </Col>
            </Row>
        </Content>
    )
}
