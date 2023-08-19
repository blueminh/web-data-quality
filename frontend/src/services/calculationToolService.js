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
    console.error('Error uploading file:', error);
    return 'An error occurred while uploading the file';
  }
}

export function getBarChartData() {
  return [
    {
        title: "Biểu đồ biến động các cấu phần của LCR",
        labels: ['2020', '2021', '2022'],
        datasets: [
            {
                label: 'Cash outflow',
                data: [10, 20, 17],
                backgroundColor: 'rgba(237,125,48,255)', // Customize the color
            },
            {
                label: 'Cash inflow',
                data: [6, 13.5, 8],
                backgroundColor: 'rgba(67,114,196,255)', // Customize the color
            },
            {
              label: 'HQLA',
              data: [5, 8, 6],
              backgroundColor: 'rgba(165,165,165,255)', // Customize the color
           },
        ]
    }, 
    {
        title: "Biểu đồ biến động cấu phần Cash outflow",
        labels: ['2020', '2021', '2022'],
        datasets: [
          {
              label: 'Rental & small business deposit',
              data: [9, 10 , 20],
              backgroundColor: 'rgba(237,125,48,255)', // Customize the color
          },
          {
              label: 'Unsecured wholesale funding',
              data: [29, 34, 16],
              backgroundColor: 'rgba(67,114,196,255)', // Customize the color
          },
          {
            label: 'Secured wholesale funding',
            data: [0, 2, 1],
            backgroundColor: 'rgba(165,165,165,255)', // Customize the color
          },
          {
            label: 'Additional requirement',
            data: [8, 4, 10],
            backgroundColor: 'rgba(237,125,48,255)', // Customize the color
          },
          {
            label: 'Other contractual funding',
            data: [0 ,1 , 4],
            backgroundColor: 'rgba(67,114,196,255)', // Customize the color
          },
          {
            label: 'Other contingen funding',
            data: [5 ,7, 6],
            backgroundColor: 'rgba(165,165,165,255)', // Customize the color
          },
      ]
    }, 
    {
        title: "Biển đồ biến động cấu phần Cash inflow",
        labels: ['2020', '2021', '2022'],
        datasets: [
            {
                label: 'Secured landing',
                data: [0, 1, 0],
                backgroundColor: 'rgba(237,125,48,255)', // Customize the color
            },
            {
                label: 'Inflows from fully performing exposures',
                data: [6, 9 , 4],
                backgroundColor: 'rgba(67,114,196,255)', // Customize the color
            },
            {
              label: 'Other cash inflows',
              data: [3, 3, 8],
              backgroundColor: 'rgba(165,165,165,255)', // Customize the color
            },
        ]
    }
  ]
}