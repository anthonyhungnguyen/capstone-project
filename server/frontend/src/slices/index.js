import { combineReducers, configureStore } from "@reduxjs/toolkit"
import auth from "./auth"
import message from "./message"
import log from "./log"

const reducer = combineReducers({ auth, message, log })

// Accept a single object because under the hook, the store has been
// configured to allow using redux devtools and redux middleware
// by default

const store = configureStore({
  reducer
})

export default store
