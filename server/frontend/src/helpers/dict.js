export function flattenNestedObject(keys, parentKey) {
  const result = {}
  for (var key in keys) {
    if (parseInt(keys[key], 10)) {
      result[parentKey + key] = keys[key]
    } else {
      flattenNestedObject(keys[key], parentKey + key + ".")
    }
  }
  return result
}
