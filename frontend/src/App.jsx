import './App.css'
import {BrowserRouter, Routes, Route} from "react-router-dom";
import LoginView from "./views/LoginView";
import MainView from "./views/MainView.jsx";
import ChooseDeptView from "./views/ChooseDeptView.jsx";
import {useState} from "react";



function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path={"/login"} element={<LoginView />}/>
                    <Route path={"/choose_dept"} element={<ChooseDeptView className={"view-dept-choose"}/>}/>
                    <Route path={"*"} element={<MainView />}/>
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
