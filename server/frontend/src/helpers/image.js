export const imgSrcToBlob = async imageSrc => {
  return new Promise(async (resolve, reject) => {
    await fetch(imageSrc)
      .then(res => resolve(res.blob()))
      .catch(reject)
  })
}
