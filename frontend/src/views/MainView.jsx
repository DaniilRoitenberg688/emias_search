import { useState, useEffect, useContext } from "react";
import { getUsers, getSearchUsers } from "../api/api.js";
import BottomMenu from "../components/BottomMenu.jsx";
import SearchBar from "../components/SearchBar";
import UserList from "../components/UserList";
import { Button, Layout, Typography } from "antd";
import {
    LogoutOutlined,
    RedditOutlined,
    UserOutlined,
} from "@ant-design/icons";
import { getGroupDoc } from "../api/group_doc.js";
import UserContext from "../contexts/UserContext.jsx";
import { serviceworker } from "globals";
import { deleteToken, getToken } from "../api/storage_api.js";

function MainView() {
    const { Header, Content, Footer } = Layout;
    const { Text, Title } = Typography;

    const [isLoading, setIsLoading] = useState(false);
    const [data, setData] = useState([]);

    const [page, setPage] = useState(0);
    const toLoad = 20;
    const [user, setUser] = useContext(UserContext);

    const [searchLine, setSearchLine] = useState("");

    const [currentUsersType, setCurrentUsersType] = useState("all_users");

    const [groupDoc, setGroupDoc] = useState([]);




    const checkLogin = async () => {
        if (localStorage.getItem("id") === null) {
            // if (user.token === null) {
            localStorage.clear();
            await deleteToken();
            window.location.href = "/login";
        }

        if (localStorage.getItem("time") === null) {
            // if (user.time === null) {
            localStorage.removeItem("id");
            return;
        }
        if (localStorage.getItem("afterLogin")) {
            localStorage.removeItem("afterLogin");
            return;
        }

        let time = parseInt(localStorage.getItem("time"));

        // const session_time = parseInt(import.meta.env.VITE_SESSION_TIME_IN_MILLISECONDS)
        // console.log(session_time)
        //
        // if (Date.now() - time > session_time) {
        //     setUser({})
        //     window.location.href = '/login'
        // }
        let token = await getToken();
        if (token === null) {
            window.location.href = "/login";
        }

        // let [status, _] = await loginRequest(userData.token).catch(err => window.location = '/login');
        //
        // if (status !== 200) {
        //     window.location.href = '/login'
        // }
    };

    const loadUsers = async (line, type) => {
        setIsLoading(true);
        let dataUsers = [];
        if (!line) {
            console.log("hier");
            if (type !== "all_users") {
                dataUsers = await getUsers(0, toLoad, type);
            }
        } else {
            console.log("cssss");
            dataUsers = await getSearchUsers(line, 0, toLoad, type);
        }
        setData(dataUsers);
        setIsLoading(false);
    };

    const onScroll = async () => {
        console.log("ssss");
        let oldData = data;
        let newData = [];
        if (!searchLine) {
            newData = await getUsers((page + 1) * toLoad, toLoad, currentUsersType);
        } else {
            newData = await getSearchUsers(
                searchLine,
                (page + 1) * toLoad,
                toLoad,
                currentUsersType,
            );
        }

        oldData.concat(newData);
        setData([...data, ...newData]);
        setPage(page + 1);
    };

    const loadGroupDocs = async () => {
        let data = await getGroupDoc();
        setGroupDoc(data);
        console.log("sdfsdf");
    };

    useEffect(() => {
        console.log("sdfjaaokdjfhjiardgh");
        checkLogin();
        loadGroupDocs();
    }, []);

    const updateSearchData = async (line) => {
        setSearchLine(line);
        await loadUsers(line, currentUsersType);
        setPage(0);
    };

    const changeUsersType = async (type) => {
        setCurrentUsersType(type);
        await loadUsers(searchLine, type);
    };

    const logout = async () => {
        await deleteToken();
        localStorage.clear();

        window.location.href = "/login";
    };


    return (
        <>
            <Layout
                style={{
                    padding: 0,
                    margin: 0,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <Header
                    style={{
                        boxSizing: "border-box",
                        backgroundColor: "#13c2c2",
                        marginBottom: "25px",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                    }}
                >
                    {/*<span>{localStorage.getItem('firstName')} {localStorage.getItem('lastName')}</span>*/}
                    <Text
                        strong={true}
                        style={{
                            color: "#fafafa",
                            lineHeight: "25px",
                            fontSize: "17px",
                        }}
                    >
                        <UserOutlined /> {localStorage.getItem("firstName")}{" "}
                        {localStorage.getItem("lastName")}
                    </Text>
                    <div>
                        <Button
                            onClick={() => {
                                window.location = "/choose_dept";
                            }}
                            variant={"solid"}
                            color={"purple"}
                            shape={"round"}
                            style={{ marginRight: "10px" }}
                        >
                            Сменить профиль <RedditOutlined />
                        </Button>

                        <Button
                            onClick={logout}
                            variant={"solid"}
                            color={"danger"}
                            shape={"round"}
                            style={{}}
                        >
                            Выйти <LogoutOutlined />
                        </Button>
                    </div>
                </Header>

                <Content style={{ flex: 1 }}>
                    <div style={{ paddingTop: "20px", paddingBottom: "20px" }}>
                        <SearchBar setLine={updateSearchData}></SearchBar>
                    </div>
                    <UserList
                        data={data}
                        isLoading={isLoading}
                        onScroll={onScroll}
                        groupDoc={groupDoc}
                    ></UserList>
                </Content>

                <Footer
                    style={{ width: "100%", padding: 0, position: "absolute", bottom: 0 }}
                >
                    <BottomMenu changeUsersType={changeUsersType} />
                </Footer>
            </Layout>
        </>
    );
}

export default MainView;
