import { Table } from "antd"
import { findAllSubjectsEnrolledByUser } from "apis/enrollment"
import { flattenNestedObject } from "helpers/dict"
import React, { useState, useEffect } from "react"
import { useSelector } from "react-redux"

export default function UserSubjects() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const { username } = useSelector(state => state.user.userData)
  useEffect(() => {
    const preprocessRawEnrollments = data => {
      const { id, groupCode, semester } = data?.subjectIDDto
      delete data["subjectIDDto"]
      return { ...data, id, groupCode, semester }
    }
    findAllSubjectsEnrolledByUser(username)
      .then(data => {
        setData(data.map(d => preprocessRawEnrollments(d)))
      })
      .catch(error => {
        setError(error)
      })
  }, [])
  const columns = [
    { title: "Semester", dataIndex: "semester", key: "semester" },
    {
      title: "ID",
      dataIndex: "id",
      key: "id"
    },
    {
      title: "Group Code",
      dataIndex: "groupCode",
      key: "groupCode"
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name"
    },
    {
      title: "Week Day",
      dataIndex: "weekDay",
      key: "weekDay"
    },
    {
      title: "Time Range",
      dataIndex: "timeRange",
      key: "timeRange"
    },
    {
      title: "Room",
      dataIndex: "room",
      key: "room"
    },
    {
      title: "Base",
      dataIndex: "base",
      key: "base"
    },
    {
      title: "Week Learn",
      dataIndex: "weekLearn",
      key: "weekLearn"
    }
  ]
  return <Table loading={data === null} dataSource={data} columns={columns} />
}
