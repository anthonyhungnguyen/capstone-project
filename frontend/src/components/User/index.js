import React, { useState } from "react"
import { Layout, Input, Row, Col, Divider } from "antd"
import styled from "styled-components"
import Info from "./Info"
import Subject from "./Subject"
import Log from "./Log"

const { Content } = Layout
const { Search } = Input

const LayoutContent = styled.div`
  background: #fff;
  padding: 24px;
  min-height: 280px;
  margin: 50px 0;
`

export function User() {
  const [id, setId] = useState("1752259")

  const onSearch = (userid) => {
    setId(userid)
  }

  return (
    <Content style={{ padding: "0 50px" }}>
      <LayoutContent>
        <Row gutter={[12, 12]}>
          <Col span={24}>
            <Search
              placeholder="enter user id"
              onSearch={onSearch}
              enterButton
              style={{ width: "20%", float: "right" }}
            />
          </Col>
          <Col span={24}>
            <Info id={id} />
          </Col>
          <Col span={12}>
            <Subject id={id} />
          </Col>
          <Col span={12}>
            <Log id={id} />
          </Col>
        </Row>
      </LayoutContent>
    </Content>
  )
}
