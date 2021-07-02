import ReactECharts from "echarts-for-react"
import React, { useEffect, useState } from "react"

export default function TeacherTimeseriesChart({ logs }) {
  const [option, setOption] = useState(null)
  useEffect(() => {
    if (logs) {
      setOption(getOption(logs))
    }
  }, [logs])
  const getOption = logs => {
    return {
      xAxis: {
        type: "time",
        splitLine: {
          show: false
        }
      },
      yAxis: {
        show: false,
        max: 0
      },
      dataZoom: {
        type: "inside"
      },
      tooltip: {
        formatter: e => {
          const data = e.data
          return `<div><p>${data[2]}</p><img src=${data[3]} style="width:150px;"/></div>`
        }
      },
      series: [
        {
          symbolSize: 20,
          data: logs.map(l => [l.timestamp, 0, l.userID, l.photo]),
          type: "scatter"
        }
      ]
    }
  }
  return option && <ReactECharts option={option} />
}
