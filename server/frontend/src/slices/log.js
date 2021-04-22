import { createSlice } from "@reduxjs/toolkit"
import { fetchLogsStudent, fetchLogsTeacher } from "apis/attendance"
import ROLE from "constants/role"
import { setMessage } from "./message"

const slice = createSlice({
  name: "user",
  initialState: {
    semesterList: [],
    semester: null,
    logs: null
  },
  reducers: {
    logsRequestSuccess: (state, action) => {
      state.logs = action.payload
    },
    logsRequestFail: (state, action) => {
      state.logs = null
      state.error = action.payload
    },
    semesterList: (state, action) => {
      state.semesterList = action.payload
    },
    semesterChange: (state, action) => {
      state.semester = action.payload
    },
    clearAll: (state, _) => {
      state.semesterList = []
      state.semester = null
      state.logs = null
    }
  }
})

export default slice.reducer

// Actions

const {
  logsRequestSuccess,
  logsRequestFail,
  semesterList,
  semesterChange,
  clearAll
} = slice.actions

const parseLogs = logs => {
  return logs.map(d => ({
    userID: d?.userID,
    subjectID: d?.subjectID,
    groupCode: d?.groupCode,
    timestamp: d?.attendanceTime,
    photo: d?.imageLink
  }))
}

const parseSemesterList = logs => {
  return [...new Set(logs.map(d => d.semester))].sort((a, b) => b - a)
}

export const logsRequest = (userid, role) => async dispatch => {
  let request
  if (role === ROLE.TEACHER) {
    request = fetchLogsTeacher(userid)
  } else if (role === ROLE.STUDENT) {
    request = fetchLogsStudent(userid)
  }
  return await request.then(
    result => {
      dispatch(logsRequestSuccess(parseLogs(result)))
      const semesters = parseSemesterList(result)
      dispatch(semesterList(semesters))
      dispatch(semesterChange(semesters[0]))
      return Promise.resolve()
    },
    error => {
      dispatch(logsRequestFail())
      dispatch(setMessage(error))
      return Promise.reject()
    }
  )
}

export const semesterRequest = semester => dispatch => {
  dispatch(semesterChange(semester))
}

export const clearAllRequest = () => dispatch => {
  dispatch(clearAll())
}
