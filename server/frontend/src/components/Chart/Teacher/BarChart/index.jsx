import React, { useEffect, useState } from "react"
import ReactECharts from "echarts-for-react"
import { useSelector } from "react-redux"
import { findStudentCountForSubjectsByTeacherID } from "apis/subject"
import axios from "axios"
import { API_PATH } from "constants/api"
import authHeader from "helpers/auth-header"

export default function BarChart() {
  const [data, setData] = useState(null)
  const { logs, schedules } = useSelector(state => state.log)
  const [option, setOption] = useState({})
  const { user } = useSelector(state => state.auth)
  const { userid } = user

  useEffect(() => {
    axios
      .get(API_PATH.TEACHER_PERCENTAGE, {
        params: {
          teacherid: userid
        },
        headers: { ...authHeader() }
      })
      .then(response => {
        if (response.data) {
          setData(response.data)
          setOption(getOption(response.data))
        } else {
          setData({})
          setOption(getOption({}))
        }
      })
  }, [])

  const getOption = data => {
    return {
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "shadow"
        }
      },
      toolbox: {
        show: true,
        orient: "vertical",
        left: "right",
        top: "center",
        feature: {
          mark: { show: true },
          dataView: { show: true, readOnly: false },
          magicType: { show: true, type: ["line", "bar", "stack", "tiled"] },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      xAxis: [
        {
          type: "category",
          axisTick: { show: false },
          data: Object.keys(data)
        }
      ],
      yAxis: [
        {
          type: "value",
          min: 0,
          max: 100
        }
      ],
      series: [
        {
          name: "Frequency",
          type: "bar",
          barGap: 0,
          emphasis: {
            focus: "series"
          },
          data: Object.values(data).map(x => x * 100)
        }
      ]
    }
  }

  return <ReactECharts option={option} showLoading={data === null} />
}
