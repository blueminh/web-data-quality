import { Tabs, Tab} from 'react-bootstrap';
import './homePage.css'
import '../../Global.css'
import CalulationQuickDashboard from '../../components/calculationTool/dashboard/dashboard';

export default function CalculationHomePage() {
    return (
        <div>
            <Tabs
                defaultActiveKey="home"
                className="mb-3"
                >
                <Tab eventKey="home" title="Home"> 
                    <CalulationQuickDashboard></CalulationQuickDashboard>
                </Tab>
                <Tab eventKey="lcr" title="LCR">
                    Tab content for LCR
                </Tab>
                <Tab eventKey="nsfr" title="NSFR">
                    Tab content for NSFR
                </Tab>
                <Tab eventKey="input" title="Input Data">
                    Tab content for inputting data
                </Tab>
            </Tabs>
        </div>
    )
}