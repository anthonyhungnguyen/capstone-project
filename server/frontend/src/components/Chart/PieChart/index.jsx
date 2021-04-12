import React from "react"
import ReactECharts from "echarts-for-react"

export default function PieChart() {
  const option = {
    title: {
      text: "Attendance Status Pie Chart",
      subText: "Fun",
      left: "center"
    },
    tooltip: {
      trigger: "item"
    },
    legend: {
      orient: "vertical",
      left: "left"
    },
    series: [
      {
        type: "pie",
        radius: "50%",
        data: [
          { value: 3, name: "On-time" },
          { value: 1, name: "Late" },
          { value: 1, name: "Miss" }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)"
          }
        }
      }
    ]
  }

  return <ReactECharts option={option} />
}
