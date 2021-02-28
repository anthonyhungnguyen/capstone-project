import PieChart from "components/Chart/PieChart"
import BarChart from "components/Chart/BarChart"
import Logs from "components/Logs"
import UserSubjects from "components/Subject/User"
import MainLayout from "layouts/MainLayout"
import React from "react"
import { Divider } from "antd"
import SemesterSelect from "components/Filter/SemesterSelect"
import DateRangePicker from "components/Filter/DateRangePicker"
import { useSelector } from "react-redux"

export default function Home() {
  const { username } = useSelector(state => state.user.userData)

  return (
    <MainLayout>
      <div className="flex justify-around">
        <div className="w-1/2 font-semibold text-lg">Hi, {username}</div>
        <div className="w-1/2 space-x-10">
          <SemesterSelect />
          <DateRangePicker />
        </div>
      </div>
      <Divider />
      <div className="flex flex-col">
        <div className="flex  justify-center space-x-10">
          <div className="w-1/3">
            <PieChart />
          </div>
          <div className="w-2/3">
            <BarChart />
          </div>
        </div>
        <div className="flex  justify-center space-x-10">
          <Logs />
          <UserSubjects />
        </div>
      </div>
    </MainLayout>
  )
}
