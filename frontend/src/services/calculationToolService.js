import axiosInstance from '../config/axiosConfig'

export async function fetchUploadHistory(username) {
  try {
    const response = await axiosInstance.get(`/upload/history?username=${username}`, {
      withCredentials: true
    });
    return response.data.upload_history;
  } catch (error) {
    console.error('Error fetching upload history:', error);
    return [];
  }
}

export async function uploadFile(data) {
  try {
    const response = await axiosInstance.post('/upload', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true
    });

    return response.data.message;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return 'Error fetching dashboard data'
  }
}

export async function getDashboardLcrNsfrData(date) {
  try {
    const response = await axiosInstance.post(`/data/getDashboardLcrNsfr`, {date}, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    console.error('Error uploading file:', error);
    return 'An error occurred while uploading the file';
  }
}

export async function getBarChartData() {
  try {
    const response = await axiosInstance.get(`/data/getDashboardBarCharts`, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    console.error('Error fetching data:', error);
    return 'Error fetching data';
  }
}

export async function getTableList() {
  try {
    const response = await axiosInstance.get(`/upload/getTableList`, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    console.error('Error fetching data:', error);
    return 'Error fetching data';
  }
}