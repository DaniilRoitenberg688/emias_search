import {Alert, Button, Card, Checkbox, ConfigProvider, Form, Input} from 'antd';
import {LockOutlined, UserOutlined} from "@ant-design/icons";
import {loginRequest} from "../api/login_api.js";
import {Buffer} from "buffer";
import {useContext, useEffect, useState} from "react";
import AppContext from "../contexts/AppContext.jsx";
import {useNavigate} from "react-router-dom";
import UserContext from "../contexts/UserContext.jsx";
import {setToken} from "../api/storage_api.js";

function LoginWindow() {
    const [error, setError] = useState(false);
    const [profiles, setProfiles] = useContext(AppContext);
    const [_, setUser] = useContext(UserContext);
    const [form] = Form.useForm();
    const navigate = useNavigate();
    Form.useWatch(() => {setError(false)}, form)

    const login = async (values) => {
        console.log(values);
        let token = Buffer.from(`${values.login}:${values.password}`, 'utf-8').toString('base64');
        console.log(token);
        let [status, data] = await loginRequest(token).catch(() => setError(true));
        if (status === 200) {
            // let userData = {
            //     'firstName': data.firstName,
            //     'lastName': data.lastName,
            //     'token': token,
            //
            // }
            localStorage.setItem('firstName', data.firstName)
            localStorage.setItem('lastName', data.lastName)
            // localStorage.setItem('remember', "1")
            let id = await setToken(token)
            localStorage.setItem('id', id)
            if (values.remember) {
                localStorage.setItem('time', Date.now())
                localStorage.setItem('afterLogin', true)
                // userData['time'] = Date.now()
                // userData['afterLogin'] = true
            }
            // setUser(userData);
            setProfiles(data['profiles']);
            navigate("/choose_dept")
        }
        else {
            setError(true);
        }


    }

    useEffect(() => {setError(false)}, [])


    return (
        <ConfigProvider theme={{token: {'colorBorderSecondary': 'rgba(0,0,0,0.22)'},}}>
            <Card style={{}} id={"loginCard"}>
                <h1 style={{"margin-bottom": '30px'}}>Вход</h1>
                <Form
                    name="basic"
                    // labelCol={{span: 8}}
                    // wrapperCol={{span: 16}}
                    initialValues={{remember: true}}
                    onFinish={login}
                    // onFinishFailed={login}
                    autoComplete="off"
                    layout={"vertical"}
                    form={form}
                >
                    <Form.Item
                        label="Логин"
                        name="login"
                        rules={[{required: true, message: 'Введите логин!'}]}
                        style={{paddingBottom: '20px'}}

                    >
                        <Input prefix={<UserOutlined/>}/>
                    </Form.Item>

                    <Form.Item
                        label="Пароль"
                        name="password"
                        rules={[{required: true, message: 'Введите пароль!'}]}
                    >
                        <Input.Password prefix={<LockOutlined/>}/>
                    </Form.Item>

                    <ConfigProvider theme={{token: {'colorPrimary': '#13c2c2'},}}>
                        <Form.Item name="remember" valuePropName="checked" label={null}>
                            <Checkbox>не выходить</Checkbox>
                        </Form.Item>
                    </ConfigProvider>

                    <Form.Item label={null}>
                        <Button variant={'solid'} htmlType="submit" color={'cyan'}>
                            Войти
                        </Button>
                    </Form.Item>
                </Form>
                {error ? <Alert message={'Проверьте данные'} showIcon={true} type={'error'} style={{marginBottom: '25px', fontSize: '15px'}}/>: null}


            </Card>
        </ConfigProvider>
    )
}

export default LoginWindow;