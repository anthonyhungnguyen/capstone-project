export const splitTimestamp = raw => {
  const splitIndex = raw.indexOf("+")
  return raw.slice(0, splitIndex)
}
