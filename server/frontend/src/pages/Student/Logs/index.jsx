import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { fetchLogs } from "apis/attendance"
import { fetchFaces, fetchFacesMetadata } from "apis/face"

export default function StudentLogs() {
  const [data, setData] = useState(null)
  const { user } = useSelector(state => state.auth)
  const { userid } = user
  useEffect(() => {
    const fetchData = async () => {
      const info = await fetchLogs(userid).then(setData)
    }
    fetchData()
  }, [])
  return (
    <MainLayout>
      <div className="space-y-4 flex items-center justify-between w-full flex-wrap">
        {data &&
          data.map(d => (
            <div>
              <img
                src={d.imageLink}
                style={{ height: "200px" }}
                alt="attendance"
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
