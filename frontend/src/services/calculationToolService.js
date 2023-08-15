import axios from 'axios';
import serverUrl from '../config';

const BASE_URL = serverUrl

export async function fetchUploadHistory(username) {
  try {
    const response = await axios.get(`${BASE_URL}/upload/history?username=${username}`, {
      withCredentials: true
    });
    return response.data.upload_history;
  } catch (error) {
    console.error('Error fetching upload history:', error);
    return [];
  }
}

export async function uploadFile(data) {
  console.log(data)
  try {
    const response = await axios.post(`${BASE_URL}/upload`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true 
    });

    return response.data.message;
  } catch (error) {
    console.error('Error uploading file:', error);
    return 'An error occurred while uploading the file.';
  }
}