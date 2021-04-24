import { Divider } from "antd"
import BarChart from "components/Chart/Teacher/BarChart"
import TeacherLogs from "components/Logs/TeacherLogs"
import SemesterSelect from "components/SemesterSelect"
import ROLE from "constants/role"
import MainLayout from "layouts/MainLayout"
import React, { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { logsRequest, scheduleRequest } from "slices/log"

export default function TeacherHome() {
  const dispatch = useDispatch()
  const { user } = useSelector(state => state.auth)
  const { userid } = user
  useEffect(() => {
    dispatch(logsRequest(userid, ROLE.TEACHER))
    dispatch(scheduleRequest(userid))
  }, [])
  return (
    <MainLayout>
      <div className="flex justify-between">
        <div className="font-semibold text-lg">Hi, {userid}</div>
        <SemesterSelect />
      </div>
      <Divider />
      <div className="flex flex-wrap justify-around">
        <div className="w-full">
          <BarChart />
        </div>
        <div className="w-full">
          <TeacherLogs />
        </div>
      </div>
    </MainLayout>
  )
}
