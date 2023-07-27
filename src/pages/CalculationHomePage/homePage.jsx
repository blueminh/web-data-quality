import { Tabs, Tab} from 'react-bootstrap';
import './homePage.css'
import '../../Global.css'
import CalulationQuickDashboard from '../../components/calculationTool/dashboard/dashboard';
import LCRDashBoard from '../../components/calculationTool/lcrBoard/lcrBoard';
import InputDashboard from '../../components/calculationTool/inputBoard/inputboard';

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
                    <LCRDashBoard></LCRDashBoard>
                </Tab>
                <Tab eventKey="nsfr" title="NSFR">
                    Tab content for NSFR
                </Tab>
                <Tab eventKey="input" title="Input Data">
                    <InputDashboard></InputDashboard>
                </Tab>
            </Tabs>
        </div>
    )
}