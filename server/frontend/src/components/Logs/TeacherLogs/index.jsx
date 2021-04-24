import { Button, Image, Input, Space, Table } from "antd"
import { fetchLogsStudent } from "apis/attendance"
import React, { useEffect, useRef, useState } from "react"
import { useSelector } from "react-redux"
import moment from "moment"
import { SearchOutlined } from "@ant-design/icons"
import TeacherSchedule from "./TeacherSchedule"
import ScheduleLogs from "./ScheduleLogs"

export default function TeacherLogs() {
  const [chosenSchedule, setChosenSchedule] = useState(null)
  return (
    <div className="flex flex-col justify-around">
      <div className="md:w-2/5 sm:w-full">
        <TeacherSchedule setChosenSchedule={setChosenSchedule} />
      </div>
      <div className="md:w-2/5 sm:w-full">
        <ScheduleLogs chosenSchedule={chosenSchedule} />
      </div>
    </div>
  )
}
