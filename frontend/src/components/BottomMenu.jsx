import {Menu} from "antd";
import {useState} from "react";

function BottomMenu({changeUsersType}) {
    const items = [
        {
            label: 'Все',
            key: 'all_users',
        },
        {
            label: 'Госпитализированные',
            key: 'hospitalized',
        },
        {
            label: 'Обратившиеся',
            key: 'applicants',
        }
    ]
    const [current, setCurrent] = useState('all_users');
    const onClick = e => {
        console.log('click ', e.key);
        setCurrent(e.key)
        changeUsersType(e.key);

    };

    return (
        <>
            <Menu onClick={onClick} style={{fontSize: '15px'}} selectedKeys={[current]} mode="horizontal" theme={"dark"} items={items}></Menu>
        </>
    )
}

export default BottomMenu;