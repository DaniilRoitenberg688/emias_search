import './App.css'
import {useState, useEffect} from 'react'
import {getUsers, getSearchUsers} from "./api.js";

import SearchBar from './components/SearchBar';
import UserList from './components/UserList';

function App() {


    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState([])

    const [page, setPage] = useState(0);
    const toLoad = 20

    const [searchLine, setSearchLine] = useState('')

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
        }
        else {
            newData = await getSearchUsers(searchLine, 0, toLoad)
        }

        oldData.concat(newData);
        setData([...data, ...newData])
        setPage(page + 1)

    }

    useEffect(() => {
        loadUsers().catch(error => {
            console.log(error)
        });
    }, [])

    const updateSearchData = async (line) => {
        setSearchLine(line)
        await loadUsers(line)
        setPage(0)
    }


    return (
        <>
            <div style={{paddingTop: '20px', paddingBottom: '20px'}}>
                <SearchBar setLine={updateSearchData}></SearchBar>
            </div>
            <UserList data={data} isLoading={isLoading} onScroll={onScroll}></UserList>
        </>
    )
}

export default App
