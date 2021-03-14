const API_ROOT = "http://localhost:8080/api"
const API_FACE = "http://localhost:5000/api"

export const API_PATH = {
  LOGIN: API_ROOT + "/auth/login",
  LOGOUT: API_ROOT + "/auth/logout",
  SIGNUP: API_ROOT + "/auth/signup",
  CROP_FACE: API_FACE + "/crop",
  ROOT_FACE: API_ROOT + "/face",
  SUBJECT: API_ROOT + "/subject",
  USER: API_ROOT + "/user",
  ENROLL: API_ROOT + "/enroll",
  TEACHER: API_ROOT + "/teacher",
  TEACHER_SUBJECTS: API_ROOT + "/teacher/schedules"
}
