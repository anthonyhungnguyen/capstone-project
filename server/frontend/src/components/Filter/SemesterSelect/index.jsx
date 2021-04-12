import React from "react"
import { Select } from "antd"

export default function SemesterSelect() {
  const { Option } = Select

  function onChange(value) {
    console.log(`selected ${value}`)
  }

  return (
    <Select
      style={{ width: 200 }}
      placeholder="Select a semester"
      optionFilterProp="children"
      onChange={onChange}
      defaultActiveFirstOption="201"
    >
      <Option value="201">201</Option>
      <Option value="200">200</Option>
      <Option value="196">196</Option>
      <Option value="195">195</Option>
    </Select>
  )
}
