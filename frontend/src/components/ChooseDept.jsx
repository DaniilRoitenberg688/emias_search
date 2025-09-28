import {Table} from "antd";
import {useContext, useEffect, useState} from "react";
import AppContext from "../contexts/AppContext.jsx";
import {useNavigate} from "react-router-dom";
import UserContext from "../contexts/UserContext.jsx";
import {loginRequest} from "../api/login_api.js";
import {getToken} from "../api/storage_api.js";

function ChooseDept() {
    const [profiles, setProfiles] = useContext(AppContext);
    const [user, setUser] = useContext(UserContext);
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const columns = [
        {
            title: "Отделение",
            dataIndex: "dept",
            key: "dept",
        },
        {
            title: "Должность",
            dataIndex: "post",
            key: "post",
        }
    ]
    const [depts, setDepts] = useState([]);
    const getDepts = async () => {
        let profilesData = profiles
        if (profiles.length === 0) {
            setIsLoading(true);
            let token = await getToken();
            let [_, resp] = await loginRequest(token);
            profilesData = resp["profiles"]
            setProfiles(resp["profiles"])
            setIsLoading(false);
        }

        console.log("getDepts");
        console.log(profiles);
        let data = []
        for (let i = 0; i < profilesData.length; i++) {
            data.push({
                key: profilesData[i].deptID,
                dept: profilesData[i].deptName,
                post: profilesData[i].post,
            })

        }
        setDepts(data)
    }
    useEffect(() => {
        getDepts();
    }, [])

    const handleRowClick = (record, index, event) => {
        // Perform actions based on the clicked row data
        localStorage.setItem("deptId", record.key)
        // let userData = user
        // userData["deptId"] = record.key
        // setUser(userData);
        navigate('/')
    };
    return (
        <>
            <div className="container-dept" style={{height: "100vh"}}>
                <Table loading={isLoading} dataSource={depts} bordered={true} style={{padding: '100px'}}
                       className={"dept-table"} pagination={false} scroll={{x: 0, y: 600}}
                       onRow={(record, rowIndex) => {
                           return {
                               onClick: (event) => handleRowClick(record, rowIndex, event), // Click event handler
                           };
                       }} columns={columns}></Table>
            </div>
        </>
    )

}

export default ChooseDept;
