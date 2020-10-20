import React from 'react'
import { BrowserRouter as Router, Link, Switch, Route } from 'react-router-dom'
import { Layout, Menu, Breadcrumb } from 'antd'
import styled from 'styled-components'
import { User } from './components/User'
import { Subject } from './components/Subject'
const { Header, Footer } = Layout

const Logo = styled.div`
	width: 120px;
	height: 31px;
	background: rgba(255, 255, 255, 0.2);
	margin: 16px 24px 16px 0;
	float: left;
`

function App() {
	return (
		<Router>
			<Layout className="layout">
				<Header>
					<Logo className="logo" />
					<Menu theme="dark" mode="horizontal" defaultSelectedKeys={[ '1' ]}>
						<Menu.Item key="1">
							<Link to="/user">User</Link>
						</Menu.Item>
						<Menu.Item key="2">
							<Link to="/subject">Subject</Link>
						</Menu.Item>
					</Menu>
				</Header>
				<Switch>
					<Route path="/user">
						<User />
					</Route>
					<Route path="/subject">
						<Subject />
					</Route>
				</Switch>
				<Footer style={{ textAlign: 'center' }}>Phuc Hung @2020</Footer>
			</Layout>
		</Router>
	)
}

export default App
