import { useState } from 'react'
import { Table, Button } from 'react-bootstrap';
import './expandableRow.css'

export default function ExpandableRow({row}) {
    const [isOpenChildren, setIsOpenChildren] = useState(false) 
    const toggleOpen = () => {
        setIsOpenChildren(!isOpenChildren)
    }
    return (
        row &&
            <>
                <tr>
                    {row.data.map(data => (
                        <td className={"depth-"+ row.depth+"-row"}>{data}</td>
                    ))}
                    <td>{row.hasChildren && <Button onClick={toggleOpen}>{isOpenChildren ? "Close" : "Open"}</Button>}</td>
                </tr>
                {row.hasChildren 
                    && isOpenChildren 
                    && 
                    row.children.map(child => 
                            <ExpandableRow row={child}></ExpandableRow>
                    )
                }
            </>
    )
}
