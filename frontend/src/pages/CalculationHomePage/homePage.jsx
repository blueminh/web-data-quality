import { Tabs, Tab} from 'react-bootstrap';
import './homePage.css'
import '../../Global.css'
import CalulationQuickDashboard from '../../components/calculationTool/dashboard/dashboard';
import LCRDashBoard from '../../components/calculationTool/lcrBoard/lcrBoard';
import InputDashboard from '../../components/calculationTool/inputBoard/inputboard';
import NSFRDashBoard from '../../components/calculationTool/nsfrBoard/nsfrBoard';
import ViewMappingAndRegulatory from '../../components/calculationTool/viewMappingAndRegulatory/viewMappingAndRegulatory';

export default function CalculationHomePage() {
    return (
        <div>
            <Tabs
                defaultActiveKey="home"
                className="mb-3"
                >
                <Tab eventKey="home" title="Tổng quan"> 
                    <CalulationQuickDashboard></CalulationQuickDashboard>
                </Tab>
                <Tab eventKey="lcr" title="LCR">
                    <LCRDashBoard></LCRDashBoard>
                </Tab>
                <Tab eventKey="nsfr" title="NSFR">
                    <NSFRDashBoard></NSFRDashBoard>
                </Tab>
                <Tab eventKey="input" title="Nhập dữ liệu">
                    <InputDashboard></InputDashboard>
                </Tab>
                <Tab eventKey="viewMappingAndRegulatory" title="Bảng Mapping và Regulatory">
                    <ViewMappingAndRegulatory></ViewMappingAndRegulatory>
                </Tab>
            </Tabs>
        </div>
    )
}