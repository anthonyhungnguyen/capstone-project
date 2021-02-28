import { combineReducers, configureStore } from "@reduxjs/toolkit"
import user from "./user"
import faceEnroll from "./faceEnroll"

const reducer = combineReducers({ user, faceEnroll })

// Accept a single object because under the hook, the store has been
// configured to allow using redux devtools and redux middleware
// by default

const store = configureStore({
  reducer
})

export default store
