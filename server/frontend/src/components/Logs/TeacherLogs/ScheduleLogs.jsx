import { Button, Image, Input, Space, Table } from "antd"
import { fetchLogsStudent } from "apis/attendance"
import React, { useEffect, useRef, useState } from "react"
import { useSelector } from "react-redux"
import moment from "moment"
import { SearchOutlined } from "@ant-design/icons"
import Highlighter from "react-highlight-words"

export default function ScheduleLogs({ chosenSchedule }) {
  const { logs } = useSelector(state => state.log)
  const [preprocessedLogs, setPreprocessedLogs] = useState(null)
  const [searchText, setSearchText] = useState("")
  const [columns, setColumns] = useState(null)
  const [searchedColumn, setSearchedColumn] = useState("")
  let searchInput = useRef(null)
  useEffect(() => {
    const preprocessMatchSchedule = chosenSchedule => {
      const { groupCode, subjectID, startTime, endTime } = chosenSchedule
      return logs.filter(l => {
        const newTimestamp = l.timestamp.split("+")[0]
        return (
          l.groupCode === groupCode &&
          l.subjectID === subjectID &&
          newTimestamp >= startTime &&
          newTimestamp <= endTime
        )
      })
    }
    if (chosenSchedule) {
      const processedLogs = preprocessMatchSchedule(chosenSchedule)
      setColumns(getColumns(processedLogs))
      setPreprocessedLogs(processedLogs)
    }
  }, [chosenSchedule])

  const getColumnSearchProps = dataIndex => ({
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters
    }) => (
      <div style={{ padding: 8 }}>
        <Input
          ref={node => {
            searchInput = node
          }}
          placeholder={`Search ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={e =>
            setSelectedKeys(e.target.value ? [e.target.value] : [])
          }
          onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
          style={{ width: 188, marginBottom: 8, display: "block" }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
            icon={<SearchOutlined />}
            size="small"
            style={{ width: 90 }}
          >
            Search
          </Button>
          <Button
            onClick={() => handleReset(clearFilters)}
            size="small"
            style={{ width: 90 }}
          >
            Reset
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              confirm({ closeDropdown: false })
              setSearchText(selectedKeys[0])
              setSearchedColumn(dataIndex)
            }}
          >
            Filter
          </Button>
        </Space>
      </div>
    ),
    filterIcon: filtered => (
      <SearchOutlined style={{ color: filtered ? "#1890ff" : undefined }} />
    ),
    onFilter: (value, record) =>
      record[dataIndex]
        ? record[dataIndex]
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase())
        : "",
    onFilterDropdownVisibleChange: visible => {
      if (visible) {
        setTimeout(() => searchInput.select(), 100)
      }
    },
    render: text =>
      searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{ backgroundColor: "#ffc069", padding: 0 }}
          searchWords={[searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ""}
        />
      ) : (
        text
      )
  })

  const handleSearch = (selectedKeys, confirm, dataIndex) => {
    confirm()
    setSearchText(selectedKeys[0])
    setSearchedColumn(dataIndex)
  }

  const handleReset = clearFilters => {
    clearFilters()
    setSearchText("")
  }

  const getColumns = logs => {
    return [
      {
        title: "Student ID",
        dataIndex: "userID",
        key: "userID",
        filters: [...new Set(logs?.map(x => x.userID))].map(x => ({
          text: x,
          value: x
        })),
        ...getColumnSearchProps("userID"),
        onFilter: (value, record) => record.userID === value
      },
      {
        title: "Subject ID",
        dataIndex: "subjectID",
        key: "subjectID",
        filters: [...new Set(logs?.map(x => x.subjectID))].map(x => ({
          text: x,
          value: x
        })),
        onFilter: (value, record) => record.subjectID === value
      },
      {
        title: "Group Code",
        dataIndex: "groupCode",
        key: "groupCode",
        filters: [...new Set(logs?.map(x => x.groupCode))].map(x => ({
          text: x,
          value: x
        })),
        onFilter: (value, record) => record.groupCode === value
      },
      {
        title: "At",
        dataIndex: "timestamp",
        key: "timestamp",
        render: d => {
          return moment(d.split("+")[0]).format("yyyy-MM-DD hh:mm:ss")
        }
      },
      {
        title: "Photo",
        dataIndex: "photo",
        key: "photo",
        render: d => (
          <Image src={d} alt="attendance" style={{ width: "120px" }} />
        )
      }
    ]
  }
  return (
    <Table
      dataSource={preprocessedLogs ?? preprocessedLogs}
      columns={columns}
    />
  )
}
