import { Tabs, Tab} from 'react-bootstrap';
import './homePage.css'
import '../../Global.css'
import ValidationDashBoard from '../../components/validationTool/ValidationBoardPage';
import InputDashboard from '../../components/validationTool/inputBoard/inputboard';
import AnalyticsBoard from '../../components/validationTool/analyticsBoard/analyticsBoards';


export default function ValidationHomePage() {
    return (
        <div>
            <Tabs
                defaultActiveKey="home"
                className="mb-3"
                >
                <Tab eventKey="home" title="Home"> 
                    <ValidationDashBoard></ValidationDashBoard>
                </Tab>
                <Tab eventKey="input" title="Input Data"> 
                    <InputDashboard></InputDashboard>
                </Tab>
                <Tab eventKey="analytics" title="Analytics"> 
                    <AnalyticsBoard></AnalyticsBoard>
                </Tab>
                
            </Tabs>
        </div>
    )
}