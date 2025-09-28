import './App.css'
import {BrowserRouter, Routes, Route} from "react-router-dom";
import LoginView from "./views/LoginView";
import MainView from "./views/MainView.jsx";
import ChooseDeptView from "./views/ChooseDeptView.jsx";
import AppContext from "./contexts/AppContext.jsx";
import {useState} from "react";
import UserContext from "./contexts/UserContext.jsx";


function App() {
    const [profiles, setProfiles] = useState([]);
    const [user, setUser] = useState({});
    return (
        <>
            <UserContext value={[user, setUser]}>
                <AppContext value={[profiles, setProfiles]}>
                    <BrowserRouter>
                        <Routes>
                            <Route path={"/login"} element={<LoginView/>}/>
                            <Route path={"/choose_dept"} element={<ChooseDeptView className={"view-dept-choose"}/>}/>
                            <Route path={"*"} element={<MainView/>}/>
                        </Routes>
                    </BrowserRouter>
                </AppContext>
            </UserContext>
        </>
    )
}

export default App
