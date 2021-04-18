import { fetchAllFaces } from "apis/face"
import { fetchUsersInfo } from "apis/user"
import FaceCard from "components/FaceCard"
import MainLayout from "layouts/MainLayout"
import React, { useEffect, useState } from "react"

export default function ManageUser() {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetchUsersInfo().then(async result => {
      const studentsOnly = result.filter(u => u.roleDtos[0].name === "STUDENT")
      console.log(studentsOnly)
      setData(studentsOnly)
    })
  }, [])
  return (
    <MainLayout>
      <div className="flex justify-around">
        {data?.map(d => (
          <div>
            <p>{d.id}</p>
            <FaceCard photo={d.registers[0]?.imageLink} />
          </div>
        ))}
      </div>
    </MainLayout>
  )
}
