import React from "react"
import ReactECharts from "echarts-for-react"
import { useSelector } from "react-redux"

export default function BarChart() {
  const { logs } = useSelector(state => state.log)
  const parseData = logs => {
    const subjectWithCount = {}
    logs?.forEach(l => {
      if (l.subjectID in subjectWithCount) {
        subjectWithCount[l.subjectID] += 1
      } else {
        subjectWithCount[l.subjectID] = 1
      }
    })
    return subjectWithCount
  }

  const tableData = parseData(logs)

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
        data: Object.keys(tableData)
      }
    ],
    yAxis: [
      {
        type: "value"
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
        data: Object.values(tableData)
      }
    ]
  }

  return <ReactECharts option={option} showLoading={logs === null} />
}
