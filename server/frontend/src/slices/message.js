import { createSlice } from "@reduxjs/toolkit"

const slice = createSlice({
  name: "message",
  initialState: {
    message: ""
  },
  reducers: {
    setMessage: (state, action) => {
      state.message = action.payload
    },
    clearMessage: (state, _) => {
      state.message = ""
    }
  }
})

export default slice.reducer

// Actions

const { setMessage, clearMessage } = slice.actions

export { setMessage, clearMessage }
