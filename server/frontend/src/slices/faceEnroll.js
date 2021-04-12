const { createSlice } = require("@reduxjs/toolkit")

const slice = createSlice({
  name: "faceEnroll",
  initialState: {
    input: null,
    rawFace: null,
    croppedFace: null,
    status: null,
    error: false,
    errorMessage: null
  },
  reducers: {
    inputUpdate: (state, action) => {
      state.input = action.payload
    },
    rawFaceUpdate: (state, action) => {
      state.rawFace = action.payload
    },
    croppedFaceUpdate: (state, action) => {
      state.croppedFace = action.payload
    },
    statusUpdate: (state, action) => {
      state.status = action.payload
    },
    errorUpdate: (state, action) => {
      state.error = true
      state.errorMessage = action.payload
    }
  }
})

export default slice.reducer

export const {
  inputUpdate,
  rawFaceUpdate,
  croppedFaceUpdate,
  statusUpdate,
  errorUpdate
} = slice.actions

export const clean = () => dispatch => {
  dispatch(inputUpdate(null))
  dispatch(rawFaceUpdate(null))
  dispatch(croppedFaceUpdate(null))
}
