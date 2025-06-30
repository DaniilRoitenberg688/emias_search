import {Menu} from "antd";
import {UserOutlined} from "@ant-design/icons";


function NavBar() {
    const items = [
        {
            // label: `${localStorage.getItem('lastName')} ${localStorage.getItem('firstName')}`,
            label: 'Roitenberg Daniil',
            icon: <UserOutlined />

        },
        {

        }
    ]

    return (<Menu></Menu>)
}

export default NavBar;