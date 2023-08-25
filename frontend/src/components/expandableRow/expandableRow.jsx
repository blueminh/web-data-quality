import { useState } from 'react'
import { Table, Button } from 'react-bootstrap';
import './expandableRow.css'
import { Bar } from 'react-chartjs-2';

export default function ExpandableRow({row}) {
    const [isOpenChildren, setIsOpenChildren] = useState(false) 
    const [isOpenChart, setIsOpenChart] = useState(false)
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

    const processVolatilityDataSelf = (row) => {
        try {
            return {
                "labels": row.volatility_data.x,
                "datasets": [
                    {
                        "label": row.code,
                        "data": row.volatility_data.y,
                        "backgroundColor": 'rgba(237,125,48,255)',
                    },
                ]
            }
        } catch (error) {
            console.log("cannot process volatility data")
            return {"x":[], "y":[]}
        }
    }

    const processVolatilityDataChildren = (row) => {
        try {
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

            return {
                "labels": row.volatility_data.x,
                "datasets": row.children.map((child, index) => {
                    const colorIndex = index % colors.length;
                    return {
                      label: child.code,
                      data: child.volatility_data.y,
                      backgroundColor: colors[colorIndex],
                    };
                }),
                
            }
        } catch (error) {
            console.log("cannot process volatility data")
            return {"x":[], "y":[]}
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
                        <Button variant="light" className="icon-button" onClick={() => {setIsOpenChart(!isOpenChart)}}>
                            <img src="/img/chart_symbol2.png" alt="Icon" className="icon" />
                        </Button>
                        {row.hasChildren && <Button variant="light" onClick={() => {setIsOpenChildren(!isOpenChildren)}}>{isOpenChildren ? "^" : ">"}</Button>}
                    </td>
                </tr>
                {isOpenChart && <tr>
                    <td colSpan={6}>
                        <div className="chart-container">
                            <div className="chart">
                                <Bar data={processVolatilityDataSelf(row)} options={getBarChartOptions("")}></Bar>
                            </div>
                            {row.hasChildren && 
                                <div className="chart">
                                    <Bar data={processVolatilityDataChildren(row)} options={getBarChartOptions("")}></Bar>
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
