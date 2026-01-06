import {Modal, List, Button, Select} from "antd";
import {
    CloseOutlined,
    FileOutlined,
    ReloadOutlined,
    ScanOutlined,
} from "@ant-design/icons";
import {deleteDocApi, getDocs, makeScan, sendDocs} from "../api/scanner_api.js";
import {useEffect, useState} from "react";
import ModalPreview from "./ModalPreview.jsx";

function ModalChooseScanner({
                                open,
                                onAddedScan,
                                data,
                                isLoading,
                                patient,
                                onClose,
                                reloadScanners,
                                groupDoc,
                                onMergeDocs
                            }) {
    const [selectedGroupDoc, setSelectedGroupDocId] = useState(0);
    const [defaultVal, setDefaultVal] = useState(null);
    const [files, setFiles] = useState([]);
    const [isPdfOpen, setPdfOpen] = useState(false)
    const [selectedFile, setSelectedFile] = useState(null);

    const changeGroupDoc = async (id) => {
        setSelectedGroupDocId(id);
        let res = await getDocs(patient.mdoc_id, id);
        setFiles(res);
    };

    const scan = async (item) => {
        let code = await makeScan(patient.mdoc_id, item, selectedGroupDoc);
        console.log(code);
        onAddedScan(code);
    };

    const mergeDocs = async () => {
        let code = await sendDocs(patient.mdoc_id, selectedGroupDoc);
        onMergeDocs(code);
    }

    const selectOptions = [];
    for (let i = 0; i < groupDoc.length; i++) {
        selectOptions.push({
            value: groupDoc[i].id,
            label: groupDoc[i].name,
        });
    }
    const deleteDoc = async (item) => {
        console.log(item);
        let status = await deleteDocApi(patient.mdoc_id, selectedGroupDoc, item);
        console.log(status);
        if (status === 204) {
            let a = files;
            a = a.filter((f) => f !== item);
            setFiles(a);
        }
    };



    const pdfOpen = async (item) => {
        setPdfOpen(true)
        setSelectedFile(item)

    }
    const pdfClose = async () => {
        setPdfOpen(false)
    }




    return (
        <>
            <Modal
                title={"Выбор сканера"}
                open={open}
                onCancel={onClose}
                footer={
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            padding: "10px 0",
                        }}
                    >
                        <Button color={"cyan"} variant={"solid"} onClick={() => {mergeDocs()}}>
                            Объединить и сохранить
                        </Button>
                        <Button color={"cyan"} variant={"outlined"} onClick={onClose}>
                            Закрыть
                        </Button>
                    </div>
                }
            >


                <ModalPreview isModalOpen={isPdfOpen} onClose={pdfClose} groupDocId={selectedGroupDoc} mDocId={patient.mdoc_id} fileName={selectedFile}></ModalPreview>



                <h3 style={{"margin-top": "30px"}}>Пациент: {patient.fio}</h3>
                <h3 style={{"margin-top": "30px"}}>Номер ИБ: {patient.ib_num}</h3>
                <h3 style={{"margin-top": "30px"}}>ВМедА ID: {patient.pacs_uid}</h3>
                <div>
                    <Select
                        style={{width: "250px"}}
                        options={selectOptions}
                        defaultValue={"Выберете тип документа"}
                        onChange={(value) => {
                            changeGroupDoc(value);
                        }}
                    ></Select>
                </div>
                <div className={"reloadButtonDiv"}>
                    <Button
                        onClick={reloadScanners}
                        color={"cyan"}
                        variant={"solid"}
                        shape={"circle"}
                        style={{display: "inline-block", marginRight: "10px"}}
                    >
                        <ReloadOutlined/>
                    </Button>
                    <h4 style={{"margin-bottom": 0, display: "inline-block"}}>
                        Сканеры:
                    </h4>
                </div>
                <List
                    loading={isLoading}
                    dataSource={data}
                    renderItem={(item, index) => (
                        <List.Item key={item.name}>
                            <List.Item.Meta
                                title={item.name}
                                description={item.scanner_type}
                            />
                            <div>
                                <Button
                                    color={"cyan"}
                                    variant={"solid"}
                                    onClick={() => {
                                        scan(item);
                                    }}
                                >
                                    <ScanOutlined/>
                                </Button>
                            </div>
                        </List.Item>
                    )}
                ></List>

                <div className={"reloadButtonDiv"}>
                    <Button
                        onClick={() => changeGroupDoc(selectedGroupDoc)}
                        color={"cyan"}
                        variant={"solid"}
                        shape={"circle"}
                        style={{display: "inline-block", marginRight: "10px"}}
                    >
                        <ReloadOutlined/>
                    </Button>
                    <h4 style={{"margin-bottom": 0, display: "inline-block"}}>
                        Отсканированные документы:{" "}
                    </h4>
                </div>
                {files.length != 0 ? (
                    <div>
                        <List
                            itemLayout="horizontal"
                            dataSource={files}
                            renderItem={(item, index) => (
                                <List.Item>
                                    <List.Item.Meta avatar={<FileOutlined/>} title={item}/>
                                    <Button
                                        onClick={() => {
                                            pdfOpen(item)
                                        }}
                                        variant="filled"
                                        color="cyan"
                                    >
                                        Посмотреть
                                    </Button>
                                    <Button
                                        onClick={() => {
                                            deleteDoc(item);
                                        }}
                                        variant="link"
                                        color="cyan"
                                    >
                                        <CloseOutlined/>
                                    </Button>
                                </List.Item>
                            )}
                        />
                    </div>
                ) : (
                    <></>
                )}
            </Modal>
        </>
    );
}

export default ModalChooseScanner;
