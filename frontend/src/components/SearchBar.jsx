import {Input, Button} from 'antd'
import {SearchOutlined} from '@ant-design/icons'


const {Search} = Input

function SearchBar() {
    return (
        <>
            <Search placeholder="input search text" enterButton={<Button color={"cyan"} variant={"solid"}><SearchOutlined style={{color: 'white'}}/></Button>} onSearch={() => {}}/>
        </>
    )
}

export default SearchBar;