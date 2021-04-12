import React from "react"
import ReactECharts from "echarts-for-react"

export default function BarChart() {
  const option = {
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow"
      }
    },
    legend: {
      data: ["On-time", "Late", "Miss"]
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
        data: ["CO3024", "CO3025", "CO3026", "CO3027", "CO3028"]
      }
    ],
    yAxis: [
      {
        type: "value"
      }
    ],
    series: [
      {
        name: "On-time",
        type: "bar",
        barGap: 0,
        emphasis: {
          focus: "series"
        },
        data: [25, 26, 30, 20, 40]
      },
      {
        name: "Late",
        type: "bar",
        emphasis: {
          focus: "series"
        },
        data: [5, 2, 4, 8, 2]
      },
      {
        name: "Miss",
        type: "bar",
        emphasis: {
          focus: "series"
        },
        data: [20, 10, 15, 10, 12]
      }
    ]
  }

  return <ReactECharts option={option} />
}
