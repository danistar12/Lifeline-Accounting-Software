export const defaultColors = {
  primary: '#10B981',    // Green
  danger: '#EF4444',     // Red
  warning: '#EAB308',    // Yellow
  info: '#3B82F6',       // Blue
  gray: '#94A3B8'        // Gray
}

export const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12,
          family: "'Inter', sans-serif"
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      padding: 12,
      titleFont: {
        size: 14,
        family: "'Inter', sans-serif",
        weight: '600'
      },
      bodyFont: {
        size: 12,
        family: "'Inter', sans-serif"
      },
      borderWidth: 0,
      cornerRadius: 8
    }
  }
}

export const lineChartDefaults = {
  ...chartDefaults,
  elements: {
    line: {
      tension: 0.4,
      borderWidth: 2
    },
    point: {
      radius: 4,
      hitRadius: 8,
      hoverRadius: 6
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 12,
          family: "'Inter', sans-serif"
        }
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        borderDash: [8, 4]
      },
      ticks: {
        font: {
          size: 12,
          family: "'Inter', sans-serif"
        }
      }
    }
  }
}

export const barChartDefaults = {
  ...chartDefaults,
  elements: {
    bar: {
      borderRadius: 4
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 12,
          family: "'Inter', sans-serif"
        }
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        borderDash: [8, 4]
      },
      ticks: {
        font: {
          size: 12,
          family: "'Inter', sans-serif"
        }
      }
    }
  }
}

export const doughnutChartDefaults = {
  ...chartDefaults,
  cutout: '75%',
  plugins: {
    ...chartDefaults.plugins,
    legend: {
      ...chartDefaults.plugins.legend,
      position: 'bottom'
    }
  }
}

export const getChartOptions = (type = 'line', customOptions = {}) => {
  const defaults = {
    line: lineChartDefaults,
    bar: barChartDefaults,
    doughnut: doughnutChartDefaults
  }[type] || chartDefaults

  return {
    ...defaults,
    ...customOptions,
    plugins: {
      ...defaults.plugins,
      ...(customOptions.plugins || {})
    }
  }
}

export const getChartDatasetDefaults = (type = 'line') => {
  const defaults = {
    line: {
      borderWidth: 2,
      pointBackgroundColor: 'white',
      pointBorderWidth: 2
    },
    bar: {
      borderRadius: 4,
      maxBarThickness: 40
    },
    doughnut: {
      borderWidth: 0
    }
  }

  return defaults[type] || {}
}

export const createChartDataset = (data, options = {}) => ({
  ...getChartDatasetDefaults(options.type),
  ...options
})
