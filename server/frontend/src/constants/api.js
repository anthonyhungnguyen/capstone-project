const API_ROOT = "/api"
const API_FACE = "/face"

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
  TEACHER_SCHEDULES: API_ROOT + "/teacher/schedules",
  TEACHER_PERCENTAGE: API_ROOT + "/teacher/percentage",
  STUDENT_LOGS: API_ROOT + "/log/student",
  TEACHER_LOGS: API_ROOT + "/log/teacher",
  USER_ALL: API_ROOT + "/user/all",
  STUDENT_SUBJECT_COUNT: API_ROOT + "/subject/count"
}
