import { useState } from 'react'
import { Table, Button } from 'react-bootstrap';
import './expandableRow.css'
import { Bar } from 'react-chartjs-2';
import { getCalculatedDataByRange } from '../../services/calculationToolService';

export default function ExpandableRow({row}) {
    const [isOpenChildren, setIsOpenChildren] = useState(false) 
    const [isOpenChart, setIsOpenChart] = useState(false)
    const [volatilityData, setVolatilityData] = useState([])
    const [volatilityDataChildren, setVolatilityDataChildren] = useState([])
    const getBarChartOptions = (title) => {
        return {
            maintainAspectRatio: false,
            scales: {
                y: {
                    maxBarThickness: 1 / 3, // Adjust as needed (proportion of 2/3)
                },
            },
            plugins: {
                title: {
                    display: true,
                    text: title, // Use the title prop here
                    fontSize: 20,
                },
            },
        };
    }
    
    const handleToggleChart = () => {
        if (isOpenChart) {
            setIsOpenChart(false)
        } else {
            const fetchData = async () => {
                try {
                    const response = await getCalculatedDataByRange(row.code, 7, "days")
                    console.log(response)
                    setVolatilityData({
                        "labels": response.dateList,
                        "datasets": [
                            {
                                "label": row.code,
                                "data": response.data,
                                "backgroundColor": 'rgba(237,125,48,255)',
                            },
                        ]
                    })
                    
                    const colors = [
                        'rgba(237, 125, 48, 255)',
                        'rgba(120, 173, 49, 255)',
                        'rgba(48, 143, 153, 255)',
                        'rgba(219, 68, 55, 255)',
                        'rgba(48, 105, 139, 255)',
                        'rgba(128, 82, 166, 255)',
                        'rgba(199, 83, 147, 255)',
                        'rgba(0, 123, 255, 255)',
                        'rgba(40, 167, 69, 255)',
                        'rgba(255, 193, 7, 255)'
                    ];

                    const childrenData = []
                    for (let index = 0; index < row.children.length; index++) {
                        const child = row.children[index];
                        const responseChild = await getCalculatedDataByRange(child.code, 7, "days")
                        const colorIndex = index % colors.length;
                        childrenData.push({
                            label: child.code,
                            data: responseChild.data,
                            backgroundColor: colors[colorIndex],
                        })
                    }
                    setVolatilityDataChildren({
                        "labels": response.dateList,
                        "datasets": childrenData,
                    })
                    setIsOpenChart(true)
                } catch (error) {
                }
            };        
            fetchData()
        }
    }

    return (
        row &&
            <>
                <tr>
                    {row.data.map(data => (
                        <td className={"depth-"+ row.depth+"-row"}>{data}</td>
                    ))}
                    <td>
                        <Button variant="light" className="icon-button" onClick={handleToggleChart}>
                            <img src="/img/chart_symbol2.png" alt="Icon" className="icon" />
                        </Button>
                        {row.hasChildren && <Button variant="light" onClick={() => {setIsOpenChildren(!isOpenChildren)}}>{isOpenChildren ? "^" : ">"}</Button>}
                    </td>
                </tr>
                {isOpenChart && <tr>
                    <td colSpan={6}>
                        <div className="chart-container">
                            <div className="chart">
                                <Bar data={volatilityData} options={getBarChartOptions("")}></Bar>
                            </div>
                            {row.hasChildren && 
                                <div className="chart">
                                    <Bar data={volatilityDataChildren} options={getBarChartOptions("")}></Bar>
                                </div>
                            }
                        </div>
                    </td>
                </tr>}
                {row.hasChildren 
                    && isOpenChildren 
                    && row.children.map(child => 
                        <ExpandableRow row={child}></ExpandableRow>
                    )
                }
            </>
    )
}
