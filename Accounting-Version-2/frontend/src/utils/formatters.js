// Currency formatter
export const formatCurrency = (value, currency = 'USD') => {
  if (typeof value !== 'number') return '0.00'
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value)
}

// Date formatter
export const formatDate = (date, format = 'short') => {
  if (!date) return ''
  
  const d = new Date(date)
  
  if (format === 'short') {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric'
    }).format(d)
  }
  
  if (format === 'long') {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(d)
  }
  
  return d.toLocaleDateString()
}

// Number formatter
export const formatNumber = (value, decimals = 0) => {
  if (typeof value !== 'number') return '0'
  
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value)
}

// Percentage formatter
export const formatPercentage = (value, decimals = 1) => {
  if (typeof value !== 'number') return '0%'
  
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value / 100)
}

// Duration formatter (for time periods)
export const formatDuration = (days) => {
  if (days < 30) return `${days} days`
  if (days < 365) {
    const months = Math.floor(days / 30)
    return `${months} month${months > 1 ? 's' : ''}`
  }
  const years = Math.floor(days / 365)
  return `${years} year${years > 1 ? 's' : ''}`
}

// Status formatter
export const formatStatus = (status) => {
  const statuses = {
    paid: 'Paid',
    pending: 'Pending',
    overdue: 'Overdue',
    draft: 'Draft',
    void: 'Void',
    partial: 'Partial'
  }
  return statuses[status.toLowerCase()] || status
}

// Account type formatter
export const formatAccountType = (type) => {
  const types = {
    asset: 'Asset',
    liability: 'Liability',
    equity: 'Equity',
    revenue: 'Revenue',
    expense: 'Expense'
  }
  return types[type.toLowerCase()] || type
}

// File size formatter
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// Phone number formatter
export const formatPhoneNumber = (phoneNumber) => {
  const cleaned = ('' + phoneNumber).replace(/\D/g, '')
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
  
  if (match) {
    return '(' + match[1] + ') ' + match[2] + '-' + match[3]
  }
  
  return phoneNumber
}

// Email formatter (mask email for privacy)
export const maskEmail = (email) => {
  if (!email) return ''
  
  const [name, domain] = email.split('@')
  const maskedName = `${name.charAt(0)}${'*'.repeat(name.length - 2)}${name.charAt(name.length - 1)}`
  
  return `${maskedName}@${domain}`
}

// Company ID formatter
export const formatCompanyId = (id) => {
  if (!id) return ''
  return `COM${id.toString().padStart(6, '0')}`
}
