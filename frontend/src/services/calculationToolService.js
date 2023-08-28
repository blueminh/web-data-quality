import axiosInstance from '../config/axiosConfig'

export async function fetchUploadHistory(username) {
  try {
    const response = await axiosInstance.get(`/upload/history?username=${username}`, {
      withCredentials: true
    });
    return response.data.upload_history;
  } catch (error) {
    throw new Error('Error fetching upload history:', error)
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
    throw new Error ('fetching dashboard data:', error);
  }
}

export async function getDashboardLcrNsfrData(date) {
  try {
    const response = await axiosInstance.post(`/data/getDashboardLcrNsfr`, {date}, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    throw new Error('Error fetching dashboard data', error);
  }
}

export async function getBarChartData() {
  try {
    const response = await axiosInstance.get(`/data/getDashboardBarCharts`, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    throw new Error('Error fetching data:', error);
  }
}

export async function getTableList() {
  try {
    const response = await axiosInstance.get(`/upload/getTableList`, {
      withCredentials: true
    });

    return response.data

  } catch (error) {
    throw new Error('Error fetching data:', error);
  }
}

export async function getLcrData(requestData) {
  try {
    const response = await axiosInstance.post(`/data/getLcr`, requestData, {
      withCredentials: true,
    });

    return response.data

  } catch (error) {
    console.log(error)
    throw new Error('Error fetching LCR data:', error);
  }
}