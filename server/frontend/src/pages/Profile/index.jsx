import { Card, Col, Row } from "antd"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { useSelector } from "react-redux"

export default function Profile() {
  const { user } = useSelector(state => state.auth)
  const { userid, accessToken, roles } = user
  return (
    <MainLayout>
      <Card title="User profile" className="mx-auto w-1/2">
        <Row justify="center">
          <Col span={12} className="font-semibold">
            ID
          </Col>
          <Col span={12}>{userid}</Col>
          <Col span={12} className="font-semibold">
            Token
          </Col>
          <Col span={12} className="break-words">
            {accessToken.substring(0, 20)}...
            {accessToken.substr(accessToken.length - 20)}
          </Col>
          <Col span={12} className="font-semibold">
            Roles
          </Col>
          <Col span={12}>
            <ul>
              {roles.map((role, index) => (
                <li key={index}>{role}</li>
              ))}
            </ul>
          </Col>
        </Row>
      </Card>
    </MainLayout>
  )
}
