import { Button, message, Upload } from "antd"
import React from "react"
import { UploadOutlined } from "@ant-design/icons"

export default function PhotoUpload() {
  const props = {
    beforeUpload: file => {
      if (file.type !== "image/png" && file.type !== "image/jpg") {
        message.error(`${file.name} is not a png file`)
      }
      return file.type === "image/png" || file.type === "image/jpg"
        ? true
        : Upload.LIST_IGNORE
    },
    onChange: info => {
      console.log(info.fileList)
    }
  }

  return (
    <Upload {...props}>
      <Button icon={<UploadOutlined />}>Upload png only</Button>
    </Upload>
  )
}
