import {Divider, List} from 'antd';
import {Button} from 'antd';
import {ScanOutlined} from '@ant-design/icons';
import InfiniteScroll from 'react-infinite-scroll-component';
import ModalChooseScanner from "./ModalChooseScanner.jsx";
import {useState} from "react";
import {getScanners} from "../api/scanner_api.js";
import ResultModal from "./ResultModal.jsx";

function UserList({data, isLoading, onScroll, groupDoc}) {
    const HEIGHT = window.screen.height
    const [isModalOpen, openModal] = useState(false)
    const [scanners, setScanners] = useState([])
    const [isScannersLoading, setIsScannersLoading] = useState(false)
    const [patient, setPatient] = useState('')
    const [resultModal, setResultModal] = useState(false)
    const [isScanOk, setIsScanOk] = useState(false)
    const [modalTitle, setModalTitle] = useState('')
    //const [subModalTitle, setSubModalTitle] = useState('')

    const onAddedScan = async (code) => {
        if (code === 200) {
            setIsScanOk(true)
            setModalTitle("Скан успешно добавлен")
        }
        else {
            setIsScanOk(false)
            setModalTitle("Что-то пошло не так")
        }
        setResultModal(true)
    }

    const onMergeDocs = async (code) => {
        if (code === 200) {
            setIsScanOk(true)
            setModalTitle("Документ успешно сохранен")
        }
        else {
            setIsScanOk(false)
            setModalTitle("Что-то пошло не так")
        }
        openModal(false)
        setResultModal(true)
    }

    const getScannersData = async () => {
        setIsScannersLoading(true)
        console.log("adf")
        let sc = await getScanners()
        console.log("skldhfjs")
        setScanners(sc)
        console.log(sc)
        // let _ = await checkAccess()

        setIsScannersLoading(false)
    }

    const filters = [{ classCode: 0x07 }];
    const getAccess = () => {
        navigator.usb
            .requestDevice({ filters: filters })
            .then((usbDevice) => {
                console.log("Product name: " + usbDevice.productName);
            })
            .catch((e) => {
                console.log("There is no device. " + e);
            });
    };

    const checkAccess = async () => {
        navigator.usb.getDevices().then((devices) => {
            let data = [];
            if (devices.length === 0) {
                getAccess()
            } else {
                devices.forEach((device) => {
                    let a = {}
                    a.name = device.productName
                    a.scanner_type = "twain"
                    data.push(a)
                });
            }
            setScanners(data)
        });
    }

    const onModalOpen = async (patientData) => {
        openModal(true)
        setPatient(patientData)
        checkAccess()
        if (!scanners.length) {
            let _ = await getScannersData()
        }
    }

    return (
        <>
            <div id="scrollableDiv"
                 style={{
                     height: '80vh',

                     overflow: 'auto',
                     scrollbarWidth: 0

                 }}>
                <InfiniteScroll
                    dataLength={data.length}
                    next={onScroll}
                    hasMore={data.length < data.length + 1}
                    loader={null}
                    endMessage={<Divider plain>It is all, nothing more 🤐</Divider>}
                    scrollableTarget="scrollableDiv"
                >
                    <List id='scrollingList' dataSource={data} size={'default'} loading={isLoading}
                          renderItem={(item, index) => (
                              <List.Item>
                                  <List.Item.Meta title={item.fio} description={
                                      <>
                                          {item.ib_num}
                                          {item.pacs_uid && ` / ${item.pacs_uid}`}
                                      </>
                                  } ></List.Item.Meta>
                                  <div>
                                      <Button color={'cyan'} variant={"solid"}
                                              onClick={() => onModalOpen(item)}><ScanOutlined/></Button>
                                  </div>
                              </List.Item>
                          )}>

                    </List>
                    <ModalChooseScanner open={isModalOpen} onCloseScan={onAddedScan} data={scanners} reloadScanners={getScannersData} isLoading={isScannersLoading} groupDoc={groupDoc} patient={patient} onMergeDocs={onMergeDocs} onClose={() => {openModal(false)}}></ModalChooseScanner>
                    <ResultModal isOpen={resultModal} onClose={() => {setResultModal(false); setIsScanOk(false)}} isOk={isScanOk} title={modalTitle} subtitle={""}></ResultModal>
                </InfiniteScroll>
            </div>
        </>

        // <>
        //
        //     <List bordered={true} loading={isLoading}>
        //         <VirtualList
        //             data={data}
        //             height={CONTAINER_HEIGHT}
        //             itemHeight={50}
        //             itemKey="data"
        //             onScroll={onScroll}
        //         >
        //             {item => (
        //                 <List.Item key={item}>
        //                     <List.Item.Meta
        //
        //                         title={item.fio}
        //                         description={item.ib_num}
        //                     />
        //                     <div><Button color={'cyan'} variant={"solid"} ><ScanOutlined /></Button></div>
        //                 </List.Item>
        //             )}
        //         </VirtualList>
        //     </List>
        //
        // </>
    )
}

export default UserList;
