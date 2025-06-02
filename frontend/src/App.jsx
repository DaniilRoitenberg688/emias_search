import './App.css'
import {useState, useEffect} from 'react'
import {getUsers} from "./api.js";

import SearchBar from './components/SearchBar';
import UserList from './components/UserList';

function App() {



    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState([])

    const [page, setPage] = useState(0);
    const toLoad = 20

    const loadUsers = async () => {
        setIsLoading(true)
        let dataUsers = await getUsers(0, toLoad)
        setData(dataUsers)
        setIsLoading(false)
    }

    const onScroll = async () => {
        let oldData = data;
        console.log(oldData);
        let newData = await getUsers((page + 1) * toLoad, toLoad)
        oldData.concat(newData);
        setData([...data, ...newData])
        setPage(page + 1)
    }

    useEffect(() => {
        loadUsers().catch(error => {
            console.log(error)
        });
    }, [])



    return (
        <>
            <div style={{ paddingTop: '20px', paddingBottom: '20px' }}>
                <SearchBar></SearchBar>
            </div>
            <UserList data={data} isLoading={isLoading} onScroll={onScroll}></UserList>
        </>
    )
}

export default App
