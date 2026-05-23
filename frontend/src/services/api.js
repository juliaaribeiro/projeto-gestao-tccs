import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function fetchList(path, params = {}) {
  const response = await api.get(path, { params })
  return response.data
}

export async function fetchItem(path) {
  const response = await api.get(path)
  return response.data
}

export async function postItem(path, payload, formData = false) {
  const config = formData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {}
  const response = await api.post(path, payload, config)
  return response.data
}

export async function patchItem(path, payload) {
  const response = await api.patch(path, payload)
  return response.data
}

export default api
