import { Card } from "antd"
import React from "react"
import { useSelector } from "react-redux"

export default function SelectSubject({ subject, setSubject }) {
  const { teachSubjects } = useSelector(state => state.user)
  return (
    <div className="flex flex-row justify-around flex-wrap">
      {teachSubjects?.map((v, i) => {
        const { id, groupCode, semester } = v.subjectIDDto
        return (
          <Card
            key={i}
            title={v.name}
            style={{ width: 350 }}
            headStyle={
              subject?.id === id &&
              subject?.semester === semester &&
              subject?.groupCode === groupCode
                ? { backgroundColor: "red", color: "white" }
                : {}
            }
            onClick={() => setSubject(v.subjectIDDto)}
          >
            <p>Subject ID: {id}</p>
            <p>Group code: {groupCode}</p>
            <p>Semester: {semester}</p>
          </Card>
        )
      })}
    </div>
  )
}
