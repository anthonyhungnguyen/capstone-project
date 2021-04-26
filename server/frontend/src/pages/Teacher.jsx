import { Divider, Tabs } from "antd"
import BarChart from "components/Teacher/BarChart.jsx"
import TeacherLineChart from "components/Teacher/LineChart.jsx"
import TeacherManage from "components/Teacher/Schedule/Manage"
import TeacherRegister from "components/Teacher/Schedule/Register"
import SemesterSelect from "components/SemesterSelect"
import TeacherTimeseriesChart from "components/Teacher/TimeSeriesChart.jsx"
import SelectSubject from "components/Teacher/SelectSubject.jsx"
import ROLE from "constants/role"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { logsRequest, scheduleRequest } from "slices/log"
import ScheduleLogs from "components/Teacher/ScheduleLogs"
const { TabPane } = Tabs

export default function TeacherHome() {
  const dispatch = useDispatch()
  const { user } = useSelector(state => state.auth)
  const { userid } = user
  useEffect(() => {
    dispatch(logsRequest(userid, ROLE.TEACHER))
    dispatch(scheduleRequest(userid))
  }, [userid, dispatch])
  const [horizontalTab, setHorizontalTab] = useState("subject")
  const [verticalTab, setVertialTab] = useState("schedule")

  const onHorizontalTabChange = tabKey => {
    setHorizontalTab(tabKey)
  }

  const onVerticalTabChange = tabKey => {
    setVertialTab(tabKey)
  }

  const [subject, setSubject] = useState(null)
  const [subjectLogs, setSubjectLogs] = useState(null)
  const [date, setDate] = useState(null)
  return (
    <MainLayout>
      <div className="flex justify-between">
        <div className="font-semibold text-lg">Hi, {userid}</div>
        <SemesterSelect />
      </div>
      <Divider />
      <Tabs defaultActiveKey={horizontalTab} onChange={onHorizontalTabChange}>
        <TabPane tab="Subject" key="subject">
          <SelectSubject setSubject={setSubject} subject={subject} />
          <Divider />
          {subject !== null ? (
            <Tabs
              defaultActiveKey={verticalTab}
              onChange={onVerticalTabChange}
              tabPosition={"left"}
            >
              <TabPane tab="Schedule" key="schedule">
                <TeacherRegister subject={subject} />
                <TeacherManage />
              </TabPane>
              <TabPane tab="Statistics" key="statistics">
                <TeacherLineChart
                  subject={subject}
                  setSubjectLogs={setSubjectLogs}
                  subjectLogs={subjectLogs}
                  setDate={setDate}
                />
                {subjectLogs && date in subjectLogs && (
                  <>
                    <TeacherTimeseriesChart logs={subjectLogs[date]} />

                    <ScheduleLogs logs={subjectLogs[date]} />
                  </>
                )}
              </TabPane>
            </Tabs>
          ) : null}
        </TabPane>
        <TabPane tab="Overview" key="overview">
          <BarChart />
        </TabPane>
      </Tabs>
    </MainLayout>
  )
}
