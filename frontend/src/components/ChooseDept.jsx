import {loginRequest} from "../api/login_api.js";
import {Table} from "antd";
import {useEffect, useState} from "react";

function ChooseDept() {
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
        let [_, resp] = await loginRequest(localStorage.getItem("token"));
        console.log("dljfksjdf");
        let profiles = resp["profiles"]
        let data = []
        for (let i = 0; i < profiles.length; i++) {
            data.push({
                key: profiles[i].deptID,
                dept: profiles[i].deptName,
                post: profiles[i].post,
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
        window.location = '/'
    };
    return (
        <>
            <div className="container-dept" style={{height: "100vh"}}>
                <Table dataSource={depts} bordered={true} style={{padding: '100px'}}
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
