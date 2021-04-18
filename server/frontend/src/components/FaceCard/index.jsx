import { convertZoneDateTime } from "helpers/time"
import React from "react"

export default function FaceCard({ photo, metadata }) {
  return (
    <div
      className="text-center m-2 p-2 border-2 shadow-sm
     rounded border-gray-300 max-w-sm flex
      items-center flex-col justify-between space-y-2"
    >
      <img src={photo} alt="face_photo" className="object-contain" />
      <p className="font-semibold">{metadata.timeCreated}</p>
      {/* <p>
        <span className="font-semibold">Status:</span> {status}
      </p> */}
    </div>
  )
}
