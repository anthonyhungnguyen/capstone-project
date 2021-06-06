import { Select } from "antd"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { semesterRequest } from "slices/log"

export default function SemesterSelect() {
  const { Option } = Select
  const dispatch = useDispatch()
  const { semesterList } = useSelector(state => state.log)

  function onChange(value) {
    dispatch(semesterRequest(value))
  }

  return (
    <Select
      style={{ width: 200 }}
      placeholder="Select a semester"
      optionFilterProp="children"
      onChange={onChange}
    >
      {semesterList.map(s => (
        <Option value={s}>{s}</Option>
      ))}
    </Select>
  )
}
