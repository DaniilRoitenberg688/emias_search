import {Modal, List, Button} from "antd";
import {ReloadOutlined, ScanOutlined} from "@ant-design/icons";
import {makeScan} from "../api/scanner_api.js";

function ModalChooseScanner({open, onCloseScan, data, isLoading, patient, onClose, reloadScanners}) {

    const scan = async (item) => {
        let code = await makeScan(patient.mdoc_id, item);
        console.log(code);
        onCloseScan(code)


    }

    return (
        <>
            <Modal title={'Выбор сканера'} open={open} onCancel={onClose} footer={<Button color={'cyan'} variant={'outlined'} onClick={onClose}>Закрыть</Button>}>
                <h3 style={{'margin-top': '30px'}}>Пациент: {patient.fio}</h3>
                <h3 style={{'margin-bottom': '30px'}}>Номер ИБ: {patient.ib_num}</h3>
                <div className={"reloadButtonDiv"}>
                    <Button onClick={reloadScanners} color={'cyan'} variant={"solid"} shape={'circle'} style={{display: "inline-block", marginRight: '10px'}}><ReloadOutlined /></Button>
                    <h4 style={{'margin-bottom': 0, 'display': 'inline-block'}}>Сканеры:</h4>
                </div>
                <List loading={isLoading} dataSource={data} renderItem={(item, index) => (
                    <List.Item key={item.name}>
                        <List.Item.Meta
                            title={item.name}
                            description={item.scanner_type}
                        />
                        <div><Button color={'cyan'} variant={"solid"} onClick={() => {scan(item)}}
                                     ><ScanOutlined/></Button></div>
                    </List.Item>
                )}>

                </List>

            </Modal>
        </>
    )
}

export default ModalChooseScanner