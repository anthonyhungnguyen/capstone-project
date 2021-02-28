import MainLayout from "layouts/MainLayout"
import React, { useState } from "react"
import ChooseInput from "components/Face/FaceEnrollSteps/ChooseInput"
import Upload from "components/Face/FaceEnrollSteps/Upload"
import { Button, Steps, message } from "antd"
import Verify from "components/Face/FaceEnrollSteps/Verify"
import Save from "components/Face/FaceEnrollSteps/Save"
import { useSelector } from "react-redux"
import "./index.css"

const { Step } = Steps

export default function FaceEnroll() {
  const [current, setCurrent] = useState(0)
  const { input, rawFace, croppedFace } = useSelector(state => state.faceEnroll)

  const next = () => {
    setCurrent(current + 1)
  }

  const prev = () => {
    setCurrent(current - 1)
  }

  const steps = [
    {
      title: "Input",
      content: <ChooseInput />,
      checkExist: input === null
    },
    {
      title: "Upload",
      content: <Upload />,
      checkExist: rawFace === null
    },
    {
      title: "Verify",
      content: <Verify />,
      checkExist: croppedFace === null
    },
    {
      title: "Save",
      content: <Save setCurrent={setCurrent} />
    }
  ]

  return (
    <MainLayout>
      <div className="flex mt-5">
        <div className="m-auto space-y-10">
          <Steps current={current}>
            {steps.map(item => (
              <Step key={item.title} title={item.title} />
            ))}
          </Steps>
          <div className="steps-content m-4 p-8 border-1 bg-gray-100 text-center">
            {steps[current].content}
          </div>
          <div className="mt-5">
            {current < steps.length - 1 && (
              <Button
                type="primary"
                onClick={() => next()}
                disabled={steps[current].checkExist}
              >
                Next
              </Button>
            )}
            {current === steps.length - 1 && (
              <Button
                type="primary"
                onClick={() => message.success("Processing complete!")}
              >
                Done
              </Button>
            )}
            {current > 0 && (
              <Button style={{ margin: "0 8px" }} onClick={() => prev()}>
                Previous
              </Button>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
