function formatDate(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('default', { dateStyle: 'short', timeStyle: 'long' }).format(date)
}

export { formatDate }
