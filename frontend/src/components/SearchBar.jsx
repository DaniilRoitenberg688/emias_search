import {Input, Button} from 'antd'
import {SearchOutlined} from '@ant-design/icons'
import {useEffect, useState} from "react";


const {Search} = Input

function SearchBar({setLine}) {
    const [timeoutId, setTimeoutId] = useState(null)
    const setOnChange = (val) => {
        clearTimeout(timeoutId)
        console.log(document.getElementById('searchBar').value)
        console.log(val)
        setTimeoutId(setTimeout(() => setLine(val), 200))
    }

    // useEffect(() => {
    //     const timeOutId = setTimeout(() => setLine(searchLine), 500);
    //     return () => clearTimeout(timeOutId);
    // }, [searchLine, setLine, setSearchLine]);

    return (
        <>
            <div id="search-bar">
                <Search placeholder="ФИО или номер ИБ" id={'searchBar'} onPressEnter={e => setOnChange(e.target.value)} onChange={e =>
                    setOnChange(e.target.value)}

                    enterButton={<Button color={"cyan"} variant={"solid"} onClick={() => (setOnChange(document.getElementById('searchBar').value))}><SearchOutlined style={{color: 'white'}}

                /></Button>}
                onSearch={() => {
                }}/>
            </div>
        </>
    )
}

export default SearchBar;