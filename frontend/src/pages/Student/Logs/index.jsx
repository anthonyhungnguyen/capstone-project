import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { fetchLogs } from "apis/attendance"

export default function StudentLogs() {
  const [data, setData] = useState(null)
  const { user } = useSelector(state => state.auth)
  const { userid } = user
  useEffect(() => {
    fetchLogs(userid).then(setData)
  }, [])
  console.log(data)

  return (
    <MainLayout>
      <div className="space-y-4 flex items-center justify-between w-full flex-wrap">
        {data &&
          data.map(d => (
            <div>
              <img
                src={`data:image/jpeg;base64,${d.imgSrcBase64}`}
                style={{ height: "200px" }}
              />
              <p>{d.semester}</p>
              <p>{d.groupCode}</p>
              <p>{d.subjectID}</p>
              <p>{d.timestamp}</p>
            </div>
          ))}
      </div>
    </MainLayout>
  )
}
