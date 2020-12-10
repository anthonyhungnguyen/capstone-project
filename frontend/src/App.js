import React, { useState } from "react"
import { BrowserRouter as Router, Link, Switch, Route } from "react-router-dom"
import { Layout, Menu, Breadcrumb } from "antd"
import styled from "styled-components"
import { User } from "./components/User"
import Timetable from "./components/Subject/Timetable"
const { Header, Footer } = Layout

const Logo = styled.div`
    width: 120px;
    height: 31px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px 24px 16px 0;
    float: left;
`

function App() {
    const [currentTab, setCurrentTab] = useState("User")

    return (
        <Router>
            <Layout className='layout'>
                <Header>
                    <Logo className='logo' />
                    <Menu
                        theme='dark'
                        mode='horizontal'
                        defaultSelectedKeys={["User"]}
                    >
                        <Menu.Item
                            key='User'
                            onClick={(e) => setCurrentTab(e.key)}
                        >
                            User
                        </Menu.Item>
                        <Menu.Item
                            key='Timetable'
                            onClick={(e) => setCurrentTab(e.key)}
                        >
                            Timetable
                        </Menu.Item>
                    </Menu>
                </Header>
                <>
                    {currentTab === "User" && <User />}
                    {currentTab === "Timetable" && <Timetable />}
                </>
                <Footer style={{ textAlign: "center" }}>Phuc Hung @2020</Footer>
            </Layout>
        </Router>
    )
}

export default App
