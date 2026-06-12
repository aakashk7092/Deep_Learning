import { acceptedImageTypes, maxUploadSize } from './constants'

export const validateEmail = (email) => /\S+@\S+\.\S+/.test(email)

export const validatePassword = (password) => password.length >= 8

export const validateAuthForm = ({ name, email, password }, mode = 'login') => {
  const errors = {}
  if (mode === 'register' && !name?.trim()) errors.name = 'Name is required.'
  if (!email?.trim()) errors.email = 'Email is required.'
  else if (!validateEmail(email)) errors.email = 'Enter a valid email address.'
  if (!password) errors.password = 'Password is required.'
  else if (!validatePassword(password)) errors.password = 'Use at least 8 characters.'
  return errors
}

export const validateImageFile = (file) => {
  if (!file) return 'Choose a plant leaf image.'
  if (!acceptedImageTypes.includes(file.type)) return 'Upload a JPG, PNG, or WebP image.'
  if (file.size > maxUploadSize) return 'Image must be smaller than 8 MB.'
  return ''
}
