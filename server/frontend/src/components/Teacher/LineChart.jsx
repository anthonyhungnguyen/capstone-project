import ReactECharts from "echarts-for-react"
import moment from "moment"
import React, { useEffect } from "react"
import { useSelector } from "react-redux"

export default function TeacherLineChart({
  subject,
  subjectLogs,
  setSubjectLogs,
  setDate
}) {
  const { logs } = useSelector(state => state.log)
  useEffect(() => {
    if (subject) {
      const result = {}
      const { id, groupCode } = subject
      logs
        .filter(l => l.subjectID === id && groupCode === l.groupCode)
        .forEach(l => {
          const date = moment(l.timestamp).format("yyyy-MM-DD")
          if (date in result) {
            result[date].push(l)
          } else {
            result[date] = [l]
          }
          return l
        })
      setSubjectLogs(result)
    }
  }, [subject, logs, setSubjectLogs])

  const handleDateClick = e => {
    setDate(e.name)
  }

  const getOption = data => {
    return {
      xAxis: {
        type: "category",
        data: Object.keys(data)
      },
      yAxis: {
        type: "value"
      },
      series: [
        {
          data: Object.values(data).map(d => d.length),
          type: "line"
        }
      ]
    }
  }
  return (
    <ReactECharts
      option={subjectLogs ? getOption(subjectLogs) : {}}
      showLoading={subjectLogs === null}
      onEvents={{
        click: handleDateClick
      }}
    />
  )
}
