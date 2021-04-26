import { createSlice } from "@reduxjs/toolkit"
import { fetchUserInfo } from "apis/user"
import { setMessage } from "./message"

const slice = createSlice({
  name: "user",
  initialState: {
    registers: [],
    roles: [],
    subjects: [],
    teachSubjects: []
  },
  reducers: {
    init: (state, action) => {
      state.registers = action.payload.registers
      state.roles = action.payload.roles
      state.subjects = action.payload.subjects
      state.teachSubjects = action.payload.teachSubjects
    }
  }
})

export default slice.reducer

// Actions

const { init } = slice.actions

export const requestUserInfo = userid => async dispatch => {
  return await fetchUserInfo(userid).then(
    data => {
      dispatch(init(data))
    },
    error => {
      dispatch(setMessage(error))
    }
  )
}
