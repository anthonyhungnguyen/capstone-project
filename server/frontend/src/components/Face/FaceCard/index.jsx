import { convertZoneDateTime } from "helpers/time"
import React from "react"

export default function FaceCard({ photo }) {
  const { base64, timestamp, status } = photo
  return (
    <div
      className="text-center m-2 p-2 border-2 shadow-sm
     rounded border-gray-300 max-w-sm flex
      items-center flex-col justify-between space-y-2"
    >
      <img src={base64} alt="face_photo" className="object-contain" />
      <p className="font-semibold">{convertZoneDateTime(timestamp)}</p>
      <p>
        <span className="font-semibold">Status:</span> {status}
      </p>
    </div>
  )
}
