export default function authHeader() {
  const user = JSON.parse(localStorage.getItem("user"))
  debugger
  if (user && user.accessToken) {
    return { Authorization: `Bearer ${user.accessToken}` }
  }
  return {}
}
