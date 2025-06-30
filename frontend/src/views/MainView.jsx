import {useState, useEffect} from 'react'
import {getUsers, getSearchUsers} from "../api/api.js";

import SearchBar from '../components/SearchBar';
import UserList from '../components/UserList';
import {Button, Layout, Typography} from "antd";
import {LogoutOutlined, UserOutlined} from "@ant-design/icons";



function MainView() {
    const {Header, Content, Footer} = Layout;
    const {Text, Title} = Typography;

    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState([])

    const [page, setPage] = useState(0);
    const toLoad = 20

    const [searchLine, setSearchLine] = useState('')

    const checkLogin = async () => {
        if (localStorage.getItem('token') === null) {
            localStorage.clear()
            window.location.href = '/login'
        }

        if (localStorage.getItem('time') === null) {
            localStorage.removeItem('token')
            return
        }
        if (localStorage.getItem('afterLogin')) {
            localStorage.removeItem('afterLogin')
            return
        }

        let time = parseInt(localStorage.getItem('time'));

        const session_time = parseInt(import.meta.env.VITE_SESSION_TIME_IN_MILLISECONDS)
        console.log(session_time)

        if (Date.now() - time > session_time) {
            localStorage.clear()
            window.location.href = '/login'
        }

        // let [status, _] = await loginRequest(userData.token).catch(err => window.location = '/login');
        //
        // if (status !== 200) {
        //     window.location.href = '/login'
        // }

    }

    const loadUsers = async (line) => {
        setIsLoading(true)
        let dataUsers = []
        if (!line) {
            dataUsers = await getUsers(0, toLoad)
        } else {
            dataUsers = await getSearchUsers(line, 0, toLoad)
        }
        setData(dataUsers)
        setIsLoading(false)
    }

    const onScroll = async () => {
        let oldData = data;
        let newData = []
        if (!searchLine) {
            newData = await getUsers((page + 1) * toLoad, toLoad)
        } else {
            newData = await getSearchUsers(searchLine, 0, toLoad)
        }

        oldData.concat(newData);
        setData([...data, ...newData])
        setPage(page + 1)

    }

    useEffect(() => {
        checkLogin()
        loadUsers().catch(error => {
            console.log(error)
        });
    }, [])

    const updateSearchData = async (line) => {
        setSearchLine(line)
        await loadUsers(line)
        setPage(0)
    }

    const logout = () => {
        localStorage.clear()
        window.location.href = '/login'
    }


    return (
        <>
            <Layout style={{ padding: 0, margin: 0 }}>
                <Header style={{boxSizing: 'border-box', backgroundColor: '#13c2c2', marginBottom: '25px', display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                    {/*<span>{localStorage.getItem('firstName')} {localStorage.getItem('lastName')}</span>*/}
                    <Text strong={true} style={{color: '#fafafa', lineHeight: '25px', fontSize: '17px'}}><UserOutlined />  {localStorage.getItem('firstName')} {localStorage.getItem('lastName')}</Text>
                    <Button onClick={logout} variant={"solid"} color={'danger'} shape={'round'} style={{}}>Выйти <LogoutOutlined /></Button>
                </Header>

                <Content>
                    <div style={{paddingTop: '20px', paddingBottom: '20px'}}>
                        <SearchBar setLine={updateSearchData}></SearchBar>
                    </div>
                    <UserList data={data} isLoading={isLoading} onScroll={onScroll}></UserList>
                </Content>
            </Layout>
        </>
    )
}

export default MainView;